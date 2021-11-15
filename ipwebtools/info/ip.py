# Copyright (c) 2021, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""IP Info Page."""
import geoip2.webservice
from ipwhois import IPWhois

from netaddr import IPAddress, AddrFormatError
from starlette_wtf import csrf_protect
from ipwebtools.forms import IPInfoForm

from ipwebtools.templates import templates

from ipwebtools.settings import GEOIP_API_KEY, GEOIP_ENABLED, GEOIP_USER_ID, GEOIP_HOST

# import pprint

# pp = pprint.PrettyPrinter(indent=2, width=120)


async def get_geoip(ip_addr):
    """Get IP Location/GeoIP data.

    Args:
        ip_addr (str): IP Address to find location data from

    Returns:
        dict: IP Location/GeoIP data
    """
    async with geoip2.webservice.AsyncClient(
        int(str(GEOIP_USER_ID)), str(GEOIP_API_KEY), host=GEOIP_HOST
    ) as client:
        try:
            result = await client.city(ip_addr)
            return result
        except Exception:
            return


async def get_ip_whois(ip_addr):
    """Get IP Whois Data.

    Args:
        ip_addr (str): IP Address to find location data from

    Returns:
        dict: IP whois data
    """
    try:
        obj = IPWhois(ip_addr)
        return obj.lookup_rdap()
    except Exception:
        return


def format_subdiv(subdiv):
    """Format subdivsion from maxmind into string.

    Args:
        subdivision (subdivision): Subdivision.

    Returns:
        str: formated subdivision
    """
    return subdiv.name + " (" + subdiv.iso_code + ")"


async def get_ip_info(ip_address):
    """Get IP Info.

    Args:
        ip_addr (str): IP Address to find IP information data from.

    Returns:
        dict: IP Information
    """
    ipdata = {}
    ip_whois_data = await get_ip_whois(ip_address)

    if ip_whois_data:
        ipdata["asn"] = ip_whois_data["asn"]
        ipdata["cidr"] = ip_whois_data["asn_cidr"]
        ipdata["rir"] = ip_whois_data["asn_registry"]
        ipdata["org"] = ip_whois_data["asn_description"]

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

            results["info"] = await get_ip_info(results["ipaddress"])

        except AddrFormatError as error:
            form.ipaddress.errors.append(error)
        except ValueError:
            form.ipaddress.errors.append("Invalid IP Address.")

    return templates.TemplateResponse("info/ip.html", {"request": request, "results": results, "form": form})
