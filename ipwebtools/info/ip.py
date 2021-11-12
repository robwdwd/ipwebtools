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

from ipwebtools.settings import GEOIP_API_KEY
import pprint

# pp = pprint.PrettyPrinter(indent=2, width=120)


async def iploc_parse(ip_addr):
    """Get IP Location data.

    Args:
        ip_addr (str): IP Address to find location data from

    Returns:
        dict: IP Location data
    """
    async with geoip2.webservice.AsyncClient(635047, GEOIP_API_KEY, host="geolite.info") as client:
        try:
            result = await client.city(ip_addr)
            # pp.pprint(result)
            return result
        except Exception as error:
            # pp.pprint(error)
            return


async def ipasn_parse(ip_addr):
    """Get IP ASN data.

    Args:
        ip_addr (str): IP Address to find location data from

    Returns:
        dict: IP ASN data
    """
    try:
        obj = IPWhois(str(ip_addr))
        return obj.lookup_rdap()
    except Exception:
        return


@csrf_protect
async def ip_info(request):
    """IP info tool page entry point."""
    results = {}

    form = await IPInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            ipaddress = IPAddress(form.ipaddress.data)

            # If IP input is not on bitmask boundry 10.1.1.1/24
            results["ipaddress"] = str(ipaddress)

            # General info
            results["version"] = ipaddress.version

            # Get IP location data
            results["info"] = await iploc_parse(str(ipaddress))
            results["asn_info"] = await ipasn_parse(str(ipaddress))

        except AddrFormatError as error:
            form.ipaddress.errors.append(error)
        except ValueError:
            form.ipaddress.errors.append("Invalid IP Address.")

    return templates.TemplateResponse("info/ip.html", {"request": request, "results": results, "form": form})
