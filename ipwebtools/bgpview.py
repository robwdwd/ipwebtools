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


async def api(url: str) -> dict:

    result = {}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            result = response.raise_for_status().json()
            pp.pprint(result)
        except httpx.HTTPError:
            return {}

    if "error" in result:
        return {}

    if "data" not in result:
        return {}

    return result["data"]


async def get_bgpview_ip_info(ip_address: str) -> dict:

    return await api("https://api.bgpview.io/ip/" + ip_address)


async def get_bgpview_prefix_info(prefix: str) -> dict:

    return await api("https://api.bgpview.io/prefix/" + prefix)


async def get_bgpview_asn_info(asn: int) -> dict:

    return await api("https://api.bgpview.io/asn/" + str(asn))


async def get_bgpview_asn_ix_info(asn: int) -> dict:

    return await api("https://api.bgpview.io/asn/" + str(asn) +'/ixs')
