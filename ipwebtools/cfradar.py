# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Cloudflare Radar API client."""


import httpx

from ipwebtools.settings import CFRADAR_API_KEY, CFRADAR_URL


async def api(url: str, params: dict | None = None) -> dict:
    """Performs an asynchronous HTTP GET request to the specified URL using an AsyncClient.
    Handles HTTP errors and returns the JSON response data if successful.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response data, or an empty dictionary if there is an error or the data is not present.
    """
    headers = {"Authorization": f"Bearer {CFRADAR_API_KEY}"}
    async with httpx.AsyncClient(headers=headers, base_url=CFRADAR_URL) as client:
        try:
            response = await client.get(url=url, params=params)

            response.raise_for_status()
            result = response.json()

        except httpx.HTTPError:
            return {}

    return {} if (result.get("errors") and len(result["errors"]) > 0) or "result" not in result else result["result"]


async def get_cfradar_ip_info(ip_address: str) -> dict:
    """Retrieves information for the specified IP address by making an asynchronous API call to the BGP View API.

    Args:
        ip_address (str): The IP address for which to retrieve information.

    Returns:
        dict:  Information for the specified IP address.
    """
    result = await api("entities/ip", {"ip": ip_address})

    return result.get("ip", {})


async def get_cfradar_prefix_info(prefix: str) -> dict:
    """Retrieves information for the specified IP prefix by making an asynchronous API call to the BGP View API.

    Args:
        prefix (str): The IP prefix for which to retrieve information.

    Returns:
        dict:  Information for the specified IP prefix.
    """
    result = await api("bgp/routes/pfx2as", {"prefix": prefix, "longestPrefixMatch": True})

    return result.get("prefix_origins", {})


async def get_cfradar_asn_info(asn: int) -> dict:
    """Retrieves information for the specified ASN by making an asynchronous API call to the BGP View API.

    Args:
        asn (int): The Autonomous System Number for which to retrieve information.

    Returns:
        dict: Information for the specified ASN.
    """

    result = await api(f"entities/asns/{asn}")

    return result.get("asn", {})
