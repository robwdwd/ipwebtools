# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""ipwebtools init."""
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from ipwebtools import settings
from ipwebtools.errors import exception_handlers
from ipwebtools.routes import routes

# Set up CSRF and Sessions middleware
# Make sure to change the keys in .env file
#
middleware = [
    Middleware(SessionMiddleware, secret_key=str(settings.SECRET_KEY), session_cookie=settings.SESSION_NAME),
    Middleware(CSRFProtectMiddleware, csrf_secret=str(settings.CSRF_SECRET)),
]

# Create the App
app = Starlette(debug=settings.DEBUG, routes=routes, middleware=middleware, exception_handlers=exception_handlers)
