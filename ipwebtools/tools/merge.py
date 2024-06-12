# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Network Prefix Merge Page."""
import re

from netaddr import AddrFormatError, IPGlob, IPNetwork, IPRange, IPSet
from starlette_wtf import csrf_protect

from ipwebtools.forms import CidrMergeForm
from ipwebtools.templates import templates


def ipset_to_cidr_list(ip_set_from):
    """Convert an IP Set into a list of cidrs.

    Args:
        ipSetFrom (IPSet): The IPSet to convert from

    Returns:
        list: List of IP CIDRs
    """
    to_list = []
    for cidr in ip_set_from.iter_cidrs():
        to_list.append(str(cidr))

    return to_list


def ipset_to_range_list(ip_set_from):
    """Convert an IP Set into a list of ip ranges.

    Args:
        ipSetFrom (IPSet): The IPSet to convert from

    Returns:
        list: List of IP Ranges
    """
    to_list = []
    for ip_range in ip_set_from.iter_ipranges():
        to_list.append(str(ip_range))

    return to_list


def parse_networks(form_field):
    """Parse networks from form textarea.

    Args:
        form_field (FormField): WTForms FormField

    Returns:
        IPSet: IPSet with the networks
    """
    nets = list(filter(None, re.split(r"[\s,]+", form_field.data)))

    nets_set = IPSet([])

    for net in nets:
        try:
            # Is a glob pattern
            if "*" in net:
                nets_set.add(IPGlob(net))
                continue

            # Is a range
            if "-" in net:
                x = net.split("-")

                if len(x) == 2:
                    nets_set.add(IPRange(x[0], x[1]))
                continue

            # Must be CIDR notation
            nets_set.add(IPNetwork(net))
        except AddrFormatError as error:
            form_field.errors.append(error)

    if len(form_field.errors) > 0:
        raise ValueError

    return nets_set


@csrf_protect
async def merge(request):
    """Network prefix merge tool page entry point."""
    results = {}

    form = await CidrMergeForm.from_formdata(request)

    if await form.validate_on_submit():
        # Form submitted and is valid
        try:
            cidrs = parse_networks(form.networks)
            exclude_cidrs = parse_networks(form.excluded)
        except ValueError:
            pass
        else:
            # Remove excluded IPs from the cidr set
            new_cidrs = cidrs - exclude_cidrs

            results["cidrs"] = ipset_to_cidr_list(new_cidrs)
            results["ranges"] = ipset_to_range_list(new_cidrs)

    return templates.TemplateResponse("tools/merge.html", {"request": request, "results": results, "form": form})
