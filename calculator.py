# calculator.py - Core functions for subnet calculation
# Author: Antonio Friesen

import math


def get_base_network_ip() -> str:
    """Reads an IPv4 base network address from the user"""
    return input("Please enter the base network (/24) IPv4 address: ")


def get_number_of_subnets() -> int:
    """Reads the number of desired subnets from the user"""
    return int(input("Please enter the number of subnets: "))


def calculate_subnets(base_network: str, number_of_subnets: int) -> tuple:
    """Calculates subnets based on the base network and number of subnets"""

    # 1. Split base network into 4 octets
    base_network_ip_parts = base_network.split(".")

    # 2. Calculate log2 and round up to next power of 2
    number_subnets_raw = math.log2(number_of_subnets)
    number_subnets_rounded = math.ceil(number_subnets_raw)

    # 3. Calculate host count per subnet
    host_count = 2 ** (8 - number_subnets_rounded)

    # 4. Calculate last octet of new subnet mask
    last_octet = 256 - host_count

    # 5. Build new subnet mask
    new_mask = f"255.255.255.{last_octet}"

    # 6. Calculate network address for each subnet
    array_subnets = []
    for subnet in range(number_of_subnets):
        array_subnets.append(
            f"{base_network_ip_parts[0]}.{base_network_ip_parts[1]}.{base_network_ip_parts[2]}.{subnet * host_count}"
        )

    # 7. Return max hosts, new mask, and all network addresses
    return (host_count - 2, new_mask, array_subnets)