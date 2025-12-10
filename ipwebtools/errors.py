# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web tools Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Error handling."""


from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette_wtf.csrf import CSRFError

from ipwebtools.templates import templates


async def http_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/generic.html.j2", {"request": request, "error": exc.detail}, status_code=exc.status_code
    )


async def csrf_redirect(request: Request, exc: HTTPException):
    return RedirectResponse(request.url, 302)


exception_handlers = {CSRFError: csrf_redirect, HTTPException: http_exception}
# exception_handlers = {HTTPException: http_exception}
# exception_handlers = {404: not_found, 500: server_error, 403: forbidden}
