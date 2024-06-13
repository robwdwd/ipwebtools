# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Convert kbps into human readable format."""



import pycountry


def iso_code_to_country(country_code: str) -> str:
    """
    Converts an ISO country code to the corresponding country name.

    Args:
        country_code (str): The ISO country code to convert to a country name.

    Returns:
        str: The name of the country corresponding to the given ISO country code, or "Unknown" if the country code is not found.
    """
    country = pycountry.countries.get(alpha_2=country_code.upper())
    return "Unknown" if country is None else country.name
