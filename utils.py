# utils.py - Shared utility functions for the subnet calculator
# Author: Antonio Friesen

from validators import validate_cidr


# ip to int
def ip_to_int(ip: str) -> int:
    """Converts ip address to int"""
    # 1. convert base_network to 32-bit integer (current_address)
    octets = ip.split(".")
    octet1 = int(octets[0]) * 16777216
    octet2 = int(octets[1]) * 65536
    octet3 = int(octets[2]) * 256
    octet4 = int(octets[3])
    ip_int = octet1 + octet2 + octet3 + octet4

    return ip_int

# int to ip
def int_to_ip(ip_int: int) -> str:
    """Converts integer to ip address"""
    octet1 = ip_int // 16777216
    octet2 = (ip_int % 16777216) // 65536
    octet3 = (ip_int % 65536) // 256
    octet4 = ip_int % 256
    network_address = f"{octet1}.{octet2}.{octet3}.{octet4}"

    return network_address


def get_network_cidr() -> tuple:
    """Reads the network CIDR"""
    # 1. read input in format "ip/prefix" (e.g. "192.168.1.0/24")
    while True:
        try:
            network_cidr = input("Please enter a valid the network CIDR: ")
            # 2. validate cidr with validate_cidr()
            if validate_cidr(network_cidr):
                # 3. if valid: split on "/" and return (ip, prefix) as tuple
                ip, prefix = network_cidr.split("/")
                return ip, int(prefix)
            # 4. if invalid: print error message and ask again
            print("Please enter a valid network CIDR!")
        except ValueError:
            print("Please enter a valid network CIDR!")