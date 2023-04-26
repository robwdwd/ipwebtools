# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""CIDR Info Page."""

from netaddr import AddrFormatError, IPAddress, IPNetwork
from starlette_wtf import csrf_protect

from ipwebtools.forms import CidrInfoForm
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
async def cidr_info(request):
    """Cidr info tool page entry point."""
    results = {}

    form = await CidrInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            cidr = IPNetwork(form.network.data)

            # If IP input is not on bitmask boundry 10.1.1.1/24
            results["cidr"] = cidr.cidr

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

        except AddrFormatError as error:
            form.network.errors.append(error)

    return templates.TemplateResponse("cidr/info.html", {"request": request, "results": results, "form": form})
