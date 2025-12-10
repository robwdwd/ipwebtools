# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""ASN Info Page."""


from starlette.requests import Request
from starlette_wtf import csrf_protect

from ipwebtools.cfradar import get_cfradar_asn_info
from ipwebtools.forms import ASNInfoForm
from ipwebtools.templates import templates


@csrf_protect
async def asn_info(request: Request):
    """ASN info tool page entry point."""
    results = {}

    form = await ASNInfoForm.from_formdata(request)

    if await form.validate_on_submit():
        try:
            asn_int = int(form.asn.data)
            results = await get_cfradar_asn_info(asn_int)

        except ValueError:
            form.asn.errors.append("Invalid ASN.")

    return templates.TemplateResponse("info/asn.html.j2", {"request": request, "results": results, "form": form})
