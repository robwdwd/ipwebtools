# Copyright (c) 2021, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Error handling."""
from ipwebtools.templates import templates


async def not_found(request, exc):
    """Page not found."""
    return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=exc.status_code)


async def server_error(request, exc):
    """Server error."""
    return templates.TemplateResponse("errors/500.html", {"request": request}, status_code=500)


exception_handlers = {404: not_found, 500: server_error}
