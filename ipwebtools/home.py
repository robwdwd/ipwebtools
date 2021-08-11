# Copyright (c) 2021, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Home page."""

from ipwebtools.templates import templates


async def home(request):
    """Home Page.

    Args:
        request (request): Web Request

    Returns:
       string: HTML Page
    """
    return templates.TemplateResponse("index.html", {"request": request})
