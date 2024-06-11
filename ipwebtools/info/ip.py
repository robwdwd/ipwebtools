# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""IP Info Page."""

import pprint
from typing import Union

from geoip2.errors import GeoIP2Error
from geoip2.models import City
from geoip2.records import Subdivision
from geoip2.webservice import AsyncClient
from netaddr import AddrFormatError, IPAddress
from starlette_wtf import csrf_protect

from ipwebtools.bgpview import get_bgpview_ip_info
from ipwebtools.forms import IPInfoForm
from ipwebtools.settings import GEOIP_API_KEY, GEOIP_ENABLED, GEOIP_HOST, GEOIP_USER_ID
from ipwebtools.templates import templates

pp = pprint.PrettyPrinter(indent=2, width=120)


async def get_geoip(ip_addr: IPAddress) -> Union[City, None]:
    """Get IP Location/GeoIP data.

    Args:
        ip_addr (IPAddress): IP Address to find location data from

    Returns:
        dict: IP Location/GeoIP data
    """
    async with AsyncClient(int(str(GEOIP_USER_ID)), str(GEOIP_API_KEY), host=GEOIP_HOST) as client:
        try:
            return await client.city(str(ip_addr))
        except GeoIP2Error:
            return


def format_subdiv(subdiv: Subdivision) -> str:
    """Format subdivsion from maxmind into string.

    Args:
        subdiv(Subdivision): Subdivision.

    Returns:
        str: formated subdivision
    """
    if subdiv.name:
        return f"{subdiv.name} ({subdiv.iso_code})"
    else:
        return ""


async def get_ip_info(ip_address: IPAddress) -> dict:
    """Get IP Info.

    Args:
        ip_addr (IPAddress): IP Address to find IP information data from.

    Returns:
        dict: IP Information
    """
    ipdata = {}

    bgpview_data = await get_bgpview_ip_info(str(ip_address))

    if bgpview_data:
        ipdata["ptr_record"] = bgpview_data["ptr_record"]
        ipdata["prefixes"] = bgpview_data["prefixes"]
        ipdata["rir"] = bgpview_data["rir_allocation"]

    # Get Data from Maxmind
    if GEOIP_ENABLED:
        geoip_data = await get_geoip(ip_address)
        if geoip_data:
            ipdata["continent"] = {"name": geoip_data.continent.name, "code": geoip_data.continent.code}
            ipdata["country"] = {"name": geoip_data.country.name, "code": geoip_data.country.iso_code}
            ipdata["city"] = geoip_data.city.name
            ipdata["org"] = geoip_data.traits.autonomous_system_organization
            ipdata["network"] = geoip_data.traits.network
            ipdata["timezone"] = geoip_data.location.time_zone
            ipdata["location"] = {"latitude": geoip_data.location.latitude, "longitude": geoip_data.location.longitude}

            if geoip_data.subdivisions:
                ipdata["region"] = ", ".join(map(format_subdiv, geoip_data.subdivisions))

    return ipdata


@csrf_protect
async def ip_info(request):
    """IP info tool page entry point."""
    results = {}

    form = await IPInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            ipaddress = IPAddress(form.ipaddress.data)

            results["ipaddress"] = str(ipaddress)

            # General info
            results["version"] = ipaddress.version

            results["info"] = await get_ip_info(ipaddress)

        except AddrFormatError as error:
            form.ipaddress.errors.append(error)
        except ValueError:
            form.ipaddress.errors.append("Invalid IP Address.")

    return templates.TemplateResponse("info/ip.html", {"request": request, "results": results, "form": form})
