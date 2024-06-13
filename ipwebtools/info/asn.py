# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""ASN Info Page."""


from starlette_wtf import csrf_protect

from ipwebtools.bgpview import get_bgpview_asn_info, get_bgpview_asn_ix_info
from ipwebtools.forms import ASNInfoForm
from ipwebtools.templates import templates


@csrf_protect
async def asn_info(request):
    """ASN info tool page entry point."""
    results = {}

    form = await ASNInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            results = await get_bgpview_asn_info(form.asn.data)
            results["ixs"] = await get_bgpview_asn_ix_info(form.asn.data)

        except ValueError:
            form.asn.errors.append("Invalid ASN.")

    return templates.TemplateResponse("info/asn.html", {"request": request, "results": results, "form": form})
