# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Create Jinja2 Templates."""

from humanize import intword
from starlette.templating import Jinja2Templates

from ipwebtools.jinja2.isotocountry import iso_code_to_country
from ipwebtools.jinja2.mpbstohuman import format_megabits_per_second
from ipwebtools.jinja2.strtodate import string_to_date
from ipwebtools.settings import CFRADAR_ENABLED

templates = Jinja2Templates(directory="ipwebtools/templates")


templates.env.filters["mbps"] = format_megabits_per_second
templates.env.filters["isocountrytoname"] = iso_code_to_country
templates.env.filters["intword"] = intword
templates.env.filters["string_to_date"] = string_to_date

templates.env.globals["CFRADAR_ENABLED"] = CFRADAR_ENABLED
