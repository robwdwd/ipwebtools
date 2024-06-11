# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Setup routes."""

from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from ipwebtools.cidr.info import cidr_info
from ipwebtools.cidr.merge import merge
from ipwebtools.cidr.split import split
from ipwebtools.home import home
from ipwebtools.info.ip import ip_info

routes = [
    Route("/", endpoint=home),
    Route("/cidr/info", endpoint=cidr_info, name="cidr_info", methods=["GET", "POST"]),
    Route("/cidr/split", endpoint=split, name="cidr_split", methods=["GET", "POST"]),
    Route("/cidr/merge", endpoint=merge, name="cidr_merge", methods=["GET", "POST"]),
    Route("/info/ip", endpoint=ip_info, name="ip_info", methods=["GET", "POST"]),
    Mount("/node", app=StaticFiles(directory="node_modules"), name="node"),
    Mount("/js", app=StaticFiles(directory="js"), name="js"),
]
