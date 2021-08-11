# Copyright (c) 2021, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Convert .env settings into starlette config."""
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PORT = config("PORT", default="8000", cast=int)
LISTEN = config("LISTEN", default="127.0.0.1")
ROOT_PATH = config("ROOT_PATH", default="")

DEBUG = config("DEBUG", cast=bool, default=False)
LOG_LEVEL = config("LOG_LEVEL", default="info")

SECRET_KEY = config("SECRET_KEY", cast=Secret)
CSRF_SECRET = config("CSRF_SECRET", cast=Secret)
SESSION_NAME = config("SESSION_NAME", default="ipwebtools_session")
