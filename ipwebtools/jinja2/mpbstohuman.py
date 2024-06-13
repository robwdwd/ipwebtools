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
    units = [" Mbps", " Gbps", " Tbps", " Pbps"]
    exp = int(math.floor(math.log(mbps, 1000)))

    return f"{round(mbps / 1000 ** exp, precision)}{units[exp]}"
