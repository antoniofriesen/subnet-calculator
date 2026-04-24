# stage2.py - Core functions for subnet calculation
# Author: Antonio Friesen

import math

from stage1 import calculate_subnets


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


def get_base_network_ip() -> str:
    """Reads an IPv4 base network address from the user"""
    while True:
        try:
            base_network = input("Please enter the base network IPv4 address: ")
            if validate_ip(base_network):
                return base_network
            print("Invalid base network IPv4 address!")
        except ValueError:
            print("Please enter a valid base network IPv4 address!")


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


def get_prefix() -> int:
    """Reads the desired prefix (8/16/24) from user"""
    while True:
        try:
            prefix = int(input("Please enter the prefix (8/16/24): "))
            if validate_prefix(prefix):
                return prefix
            print("Invalid prefix!")
        except ValueError:
            print("Please enter the integer 8 or 16 or 24!")

def validate_ip(ip: str) -> bool:
    """Validates ip address"""
    # 1. trim input
    trimmed_ip = ip.strip()
    if trimmed_ip == "0.0.0.0":
        return False

    # 2. split on "."
    split_ip = trimmed_ip.split(".")

    # 3. check if exactly 4 parts
    if len(split_ip) != 4:
        return False

    # 4. for each part: trim, check if digit, check if 0-255
    for part in split_ip:
        if not part.isdigit():
            return False
        if  int(part) < 0 or int(part) > 255:
            return False

    # 5. return True if valid, False otherwise
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

