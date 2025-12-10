# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""IP Info Page."""



import pycountry
from geoip2.errors import GeoIP2Error
from geoip2.records import Subdivision
from geoip2.webservice import AsyncClient
from netaddr import AddrFormatError, IPAddress
from starlette.requests import Request
from starlette_wtf import csrf_protect

from ipwebtools.cfradar import get_cfradar_ip_info
from ipwebtools.forms import IPInfoForm
from ipwebtools.settings import (
    CFRADAR_ENABLED,
    GEOIP_API_KEY,
    GEOIP_ENABLED,
    GEOIP_HOST,
    GEOIP_USER_ID,
)
from ipwebtools.templates import templates


def get_country_name(country_code: str) -> str:
    """Get full country name from ISO country code.

    Args:
        country_code (str): ISO 2-letter country code (e.g., 'US', 'GB', 'FR')

    Returns:
        str: Full country name, or the original code if not found
    """
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name if country else country_code
    except (AttributeError, KeyError):
        return country_code


def format_subdiv(subdiv: Subdivision) -> str:
    """Format subdivsion from maxmind into string.

    Args:
        subdiv(Subdivision): Subdivision.

    Returns:
        str: formated subdivision
    """
    return f"{subdiv.name}" if subdiv.name else ""


async def get_geoip(ip_addr: str) -> dict:
    """Get IP Location/GeoIP data.

    Args:
        ip_addr (str): IP Address to find location data from

    Returns:
        City: IP Location/GeoIP data
    """
    async with AsyncClient(int(str(GEOIP_USER_ID)), str(GEOIP_API_KEY), host=GEOIP_HOST) as client:

        try:
            geoip_data = await client.city(ip_addr)

            return {
                "continent": {"name": geoip_data.continent.name, "code": geoip_data.continent.code},
                "country": {"name": geoip_data.country.name, "code": geoip_data.country.iso_code},
                "city": geoip_data.city.name,
                "org": geoip_data.traits.autonomous_system_organization,
                "network": geoip_data.traits.network,
                "timezone": geoip_data.location.time_zone,
                "location": {"latitude": geoip_data.location.latitude, "longitude": geoip_data.location.longitude},
                "region": ", ".join(map(format_subdiv, geoip_data.subdivisions)) if geoip_data.subdivisions else None,
            }
        except GeoIP2Error:
            return {}


async def get_ip_info(ip_address: str) -> dict:
    """Get IP Info.

    Args:
        ip_addr (str): IP Address to find IP information data from.

    Returns:
        dict: IP Information
    """
    ipdata = {}
    if CFRADAR_ENABLED:
        cfradar_data = await get_cfradar_ip_info(ip_address)

        if cfradar_data:
            asn_location = cfradar_data.get("asnLocation")
            ipdata |= {
                "asn": cfradar_data.get("asn"),
                "asnLocation": asn_location,
                "asnLocationName": get_country_name(asn_location) if asn_location else asn_location,
                "asnName": cfradar_data.get("asnName"),
                "asnOrgName": cfradar_data.get("asnOrgName"),
            }

    # Get Data from Maxmind and merge it with our data.
    if GEOIP_ENABLED:
        ipdata |= await get_geoip(ip_address)

    return ipdata


@csrf_protect
async def ip_info(request: Request):
    """IP info tool page entry point."""
    results = {}

    form = await IPInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            ipaddress = IPAddress(str(form.ipaddress.data).strip())
            ip_str = str(ipaddress)
            results = {"ipaddress": ip_str, "version": ipaddress.version, "info": await get_ip_info(ip_str)}

        except (AddrFormatError, ValueError):
            form.ipaddress.errors.append(f"{form.ipaddress.data} is not a valid IP Address.")

    return templates.TemplateResponse("info/ip.html.j2", {"request": request, "results": results, "form": form})
