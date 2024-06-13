# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Convert kbps into human readable format."""

from typing import Union

import pycountry


def iso_code_to_country(country_code: str) -> Union[str, None]:

    country = pycountry.countries.get(alpha_2=country_code.upper())
    return "Unknown" if country is None else country.name
