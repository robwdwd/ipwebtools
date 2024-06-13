# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Convert kbps into human readable format."""

import math
from typing import Union


def format_megabits_per_second(mbps: int, precision: Union[int, None] = None) -> str:
    """
    Formats a given speed in Megabits per second to a human-readable string with appropriate units.

    Args:
        mbps (int): The speed in Megabits per second to format.
        precision (Union[int, None], optional): The number of decimal places to round to. Defaults to None.

    Returns:
        str: The formatted speed with the appropriate unit (Mbps, Gbps, Tbps, or Pbps) or empty string if mbps is zero
    """

    if not mbps:
        return ""

    units = [" Mbps", " Gbps", " Tbps", " Pbps"]
    exp = int(math.floor(math.log(mbps, 1000)))

    return f"{round(mbps / 1000 ** exp, precision)}{units[exp]}"
