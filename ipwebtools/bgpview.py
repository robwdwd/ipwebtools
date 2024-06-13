# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""BGP View API client."""


import httpx


async def api(url: str) -> dict:
    """Performs an asynchronous HTTP GET request to the specified URL using an AsyncClient.
    Handles HTTP errors and returns the JSON response data if successful.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response data, or an empty dictionary if there is an error or the data is not present.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            result = response.json()
        except httpx.HTTPError:
            return {}

    return {} if "error" in result or "data" not in result else result["data"]


async def get_bgpview_ip_info(ip_address: str) -> dict:
    """Retrieves information for the specified IP address by making an asynchronous API call to the BGP View API.

    Args:
        ip_address (str): The IP address for which to retrieve information.

    Returns:
        dict:  Information for the specified IP address.
    """
    return await api(f"https://api.bgpview.io/ip/{ip_address}")


async def get_bgpview_prefix_info(prefix: str) -> dict:
    """Retrieves information for the specified IP prefix by making an asynchronous API call to the BGP View API.

    Args:
        prefix (str): The IP prefix for which to retrieve information.

    Returns:
        dict:  Information for the specified IP prefix.
    """
    return await api(f"https://api.bgpview.io/prefix/{prefix}")


async def get_bgpview_asn_info(asn: int) -> dict:
    """Retrieves information for the specified ASN by making an asynchronous API call to the BGP View API.

    Args:
        asn (int): The Autonomous System Number for which to retrieve information.

    Returns:
        dict: Information for the specified ASN.
    """

    return await api(f"https://api.bgpview.io/asn/{asn}")


async def get_bgpview_asn_ix_info(asn: int) -> dict:
    """Retrieves exchange point information for the specified ASN by making an
       asynchronous API call to the BGP View API.

    Args:
        asn (int): The Autonomous System Number for which to retrieve information.

    Returns:
        dict: Information for the specified ASNs exchange point connections.
    """
    return await api(f"https://api.bgpview.io/asn/{asn}/ixs")
