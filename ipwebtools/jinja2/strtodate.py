# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Convert kbps into human readable format."""

from datetime import datetime
from typing import Union

from humanize import naturaldate


def string_to_date(date: str) -> Union[str, None]:
    """
    Converts a string representation of a date to a more natural date format.

    Args:
        date (str): The string representing the date in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
        Union[str, None]: The natural language representation of the input date, or None if the conversion fails.
    """

    return naturaldate(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
