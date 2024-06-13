# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Prefix Info Page."""

from netaddr import AddrFormatError, IPAddress, IPNetwork
from starlette_wtf import csrf_protect

from ipwebtools.bgpview import get_bgpview_prefix_info
from ipwebtools.forms import PrefixInfoForm
from ipwebtools.templates import templates


def get_useable(network):
    """Work out the first and last useable addresses in a subnet.

    Args:
        network (IPNetwork): IP Network to use

    Returns:
        tuple: Returns the first and last IP in the network as a tuple.
    """
    # IPv4
    if network.version == 4:
        if network.size >= 4:
            return (IPAddress(network.first + 1), IPAddress(network.last - 1))
        else:
            return (IPAddress(network.first), IPAddress(network.last))
    # IPv6
    else:
        if network.size >= 4:
            # Done include router anycast address.
            return (IPAddress(network.first + 1), IPAddress(network.last))
        else:
            return (IPAddress(network.first), IPAddress(network.last))


@csrf_protect
async def prefix_info(request):
    """Prefix info tool page entry point."""
    results = {}

    form = await PrefixInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            cidr_str = str(form.network.data)
            cidr = IPNetwork(cidr_str.strip())

            # If IP input is not on bitmask boundry 10.1.1.1/24
            results["cidr"] = cidr.cidr

            results["info"] = await get_bgpview_prefix_info(str(cidr.cidr))

            # General info
            results["version"] = cidr.version
            results["total_ips"] = cidr.size
            results["network_mask"] = cidr.netmask
            results["host_mask"] = cidr.hostmask

            if cidr.version == 4:
                results["network_addr"] = cidr.network
                results["broadcast_addr"] = cidr.broadcast

            # First and last usable addresses
            (results["first"], results["last"]) = get_useable(cidr)

        except (AddrFormatError, ValueError):
            form.network.errors.append(f"{form.network.data} is not a valid IP Prefix")

    return templates.TemplateResponse("info/prefix.html", {"request": request, "results": results, "form": form})
