# Copyright (c) 2021, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Setup routes."""

from starlette.routing import Route

from ipwebtools.home import home
from ipwebtools.cidr.info import info
from ipwebtools.cidr.split import split
from ipwebtools.cidr.merge import merge

routes = [
    Route("/", endpoint=home),
    Route("/cidr/info", endpoint=info, name="cidr_info", methods=["GET", "POST"]),
    Route("/cidr/split", endpoint=split, name="cidr_split", methods=["GET", "POST"]),
    Route("/cidr/merge", endpoint=merge, name="cidr_merge", methods=["GET", "POST"]),
]
