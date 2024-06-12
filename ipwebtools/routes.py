# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Setup routes."""

from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from ipwebtools.home import home
from ipwebtools.info.asn import asn_info
from ipwebtools.info.ip import ip_info
from ipwebtools.info.prefix import prefix_info
from ipwebtools.tools.merge import merge
from ipwebtools.tools.split import split

routes = [
    Route("/", endpoint=home),
    Route("/info/asn", endpoint=asn_info, name="asn_info", methods=["GET", "POST"]),
    Route("/info/ip", endpoint=ip_info, name="ip_info", methods=["GET", "POST"]),
    Route("/info/prefix", endpoint=prefix_info, name="prefix_info", methods=["GET", "POST"]),
    Route("/tools/split", endpoint=split, name="cidr_split", methods=["GET", "POST"]),
    Route("/tools/merge", endpoint=merge, name="cidr_merge", methods=["GET", "POST"]),
    Mount("/node", app=StaticFiles(directory="node_modules"), name="node"),
    Mount("/js", app=StaticFiles(directory="js"), name="js"),
]
