# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Prefix Info Page."""

from netaddr import AddrFormatError, IPAddress, IPNetwork
from starlette.requests import Request
from starlette_wtf import csrf_protect

from ipwebtools.cfradar import get_cfradar_prefix_info
from ipwebtools.forms import PrefixInfoForm
from ipwebtools.settings import CFRADAR_ENABLED
from ipwebtools.templates import templates


def get_useable(network: IPNetwork):
    """Work out the first and last useable addresses in a subnet.

    Args:
        network (IPNetwork): IP Network to use

    Returns:
        tuple: Returns the first and last IP in the network as a tuple.
    """
    first_ip = IPAddress(network.first + 1) if network.size >= 4 else IPAddress(network.first)
    last_ip = IPAddress(network.last - 1) if network.version == 4 and network.size >= 4 else IPAddress(network.last)
    return (first_ip, last_ip)


async def process_ip_prefix(ip_prefix: str) -> dict:
    """Process CIDR string and return IPNetwork object."""

    ip_network = IPNetwork(ip_prefix.strip())

    first, last = get_useable(ip_network)

    info = {}

    if CFRADAR_ENABLED:
        info = await get_cfradar_prefix_info(str(ip_network.cidr))

    return {
        "cidr": ip_network.cidr,
        "info": info,
        "version": ip_network.version,
        "total_ips": ip_network.size,
        "network_mask": ip_network.netmask,
        "host_mask": ip_network.hostmask,
        "first": first,
        "last": last,
    }


@csrf_protect
async def prefix_info(request: Request):
    """Prefix info tool page entry point."""

    results = {}
    form = await PrefixInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            results = await process_ip_prefix(str(form.network.data))

        except (AddrFormatError, ValueError):
            form.network.errors.append(f"{form.network.data} is not a valid IP Prefix")

    return templates.TemplateResponse("info/prefix.html.j2", {"request": request, "results": results, "form": form})
