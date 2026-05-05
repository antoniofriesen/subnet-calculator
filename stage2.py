# stage2.py - Core functions for subnet calculation
# Author: Antonio Friesen

import math

from stage1 import calculate_subnets
from validators import validate_ip


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


def get_number_of_subnets() -> int:
    """Reads the number of desired subnets from the user"""
    while True:
        try:
            number_of_subnets = int(input("Please enter the number of subnets: "))
            if validate_number_subnets(number_of_subnets):
                return number_of_subnets
            print("Invalid number of subnets! Must be between 1 and 128!")
        except ValueError:
            print("Please enter a valid number of subnets!")


def validate_cidr(cidr: str) -> bool:
    """Validates the network CIDR"""
    # 1. trim input
    trimmed_cidr = cidr.strip()

    # 2. check if "/" exists in input
    if "/" not in trimmed_cidr:
        return False

    # 3. split on "/" into ip and prefix parts
    ip, prefix = trimmed_cidr.split("/")

    # 4. validate ip part with validate_ip()
    if not validate_ip(ip):
        return False

    # 5. validate prefix part with validate_prefix()
    try:
        if not validate_prefix(int(prefix)):
            return False
    except ValueError:
        return False

    # 6. check if ip matches prefix (e.g. /24 -> last octet must be 0)
    split_ip = ip.split(".")
    if int(prefix) == 8 and (split_ip[1] != "0" or split_ip[2] != "0" or split_ip[3] != "0"):
        return False

    if int(prefix) == 16 and (split_ip[2] != "0" or split_ip[3] != "0"):
        return False

    if int(prefix) == 24 and split_ip[3] != "0":
        return False

    # 7. return True if valid, False otherwise
    return True


def validate_number_subnets(number_subnets: int) -> bool:
    """Validates number of subnets"""
    # 1. check if number_of_subnets >= 1 or check if number_of_subnets <= 128
    if number_subnets <= 0 or number_subnets > 128:
        return False

    # 2. return True if valid, False otherwise
    return True


def validate_prefix(prefix: int) -> bool:
    """Validates ip address"""
    # 1. check if prefix not 8, 16 or 24
    if prefix not in [8, 16, 24]:
        return False

    # 2. return True if valid, False otherwise
    return True

