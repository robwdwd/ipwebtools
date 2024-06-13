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

    return naturaldate(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

