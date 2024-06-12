# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Network prefix split page."""

from netaddr import AddrFormatError, IPNetwork
from starlette_wtf import csrf_protect

from ipwebtools.forms import CidrSplitForm
from ipwebtools.templates import templates


def validate_split_fields(form):
    """Validate fields on the CIDR split form.

    Args:
        form (Form): WTForm being proccessed

    Returns:
        list|None: Resulting subnet list or None
    """
    to_prefix_len = int(form.mask.data)

    try:
        cidr = IPNetwork(form.network.data)
        if cidr.version == 4:
            if to_prefix_len > 32:
                form.mask.errors.append("Invalid prefix length for IPv4 CIDR.")
                return

        if cidr.prefixlen >= to_prefix_len:
            form.mask.errors.append("Split prefix length must be bigger than CIDR prefix length.")
            return

        return cidr.subnet(to_prefix_len)

    except AddrFormatError as error:
        form.network.errors.append(error)
        return


@csrf_protect
async def split(request):
    """Network prefix split tool page entry point."""
    results = None

    form = await CidrSplitForm.from_formdata(request)

    if await form.validate_on_submit():
        results = validate_split_fields(form)

    return templates.TemplateResponse("tools/split.html", {"request": request, "results": results, "form": form})
