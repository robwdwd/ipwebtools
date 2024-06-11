# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""BGP View API client."""

import pprint

import httpx

pp = pprint.PrettyPrinter(indent=2, width=120)


async def get_bgpview_ip_info(ip_address: str) -> dict:

    result = {}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.bgpview.io/ip/" + ip_address)
            result = response.raise_for_status().json()
        except httpx.HTTPError as exc:
            print(f"Error while requesting {exc}.")

    if "error" in result:
        return {}

    if "data" not in result:
        return {}

    return result["data"]


async def get_bgpview_prefix_info(prefix: str) -> dict:

    result = {}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.bgpview.io/prefix/" + prefix)
            result = response.raise_for_status().json()
        except httpx.HTTPError as exc:
            print(f"Error while requesting {exc}.")

    if "error" in result:
        return {}

    if "data" not in result:
        return {}

    return result["data"]
