# stage2.py - Core functions for subnet calculation
# Author: Antonio Friesen

import math

from stage1 import calculate_subnets


def get_prefix() -> int:
    """Reads the desired prefix (8/16/24) from user"""
    return int(input("Please enter the prefix (8/16/24): "))


def calculate_subnets_extended(base_network: str, prefix: int, number_of_subnets: int) -> tuple:
    """Calculates subnets based in the base network, prefix and number of subnets"""
    base_network_ip = base_network.split(".")

    if prefix == 8:
        # calculate number of subnets
        number_subnets = math.ceil((math.log2(number_of_subnets)))

        # calculate number of hosts per new subnet
        host_count = 2 ** (8 - number_subnets) * 256 * 256

        # calculate 3. octet new mask
        octet = 256 - 2 ** (8 - number_subnets)

        # build new mask
        new_mask = f"255.{octet}.0.0"

        # calculate network address for each subnet
        array_subnets = []
        for subnet in range(number_of_subnets):
            array_subnets.append(
                f"{base_network_ip[0]}."
                f"{subnet * 2 ** (8 - number_subnets)}."
                f"{base_network_ip[2]}."
                f"{base_network_ip[3]}"
            )

        return (host_count - 2, new_mask, array_subnets)
    if prefix == 16:
        # calculate number of subnets
        number_subnets = math.ceil((math.log2(number_of_subnets)))

        # calculate number of hosts per new subnet
        host_count = 2 ** (8 - number_subnets) * 256

        # calculate 3. octet new mask
        octet = 256 - 2 ** (8 - number_subnets)

        # build new mask
        new_mask = f"255.255.{octet}.0"

        # calculate network address for each subnet
        array_subnets = []
        for subnet in range(number_of_subnets):
            array_subnets.append(
                f"{base_network_ip[0]}."
                f"{base_network_ip[1]}."
                f"{subnet * 2 ** (8 - number_subnets)}."
                f"{base_network_ip[3]}"
            )

        return (host_count - 2, new_mask, array_subnets)

    if prefix == 24:
        return calculate_subnets(base_network, number_of_subnets)