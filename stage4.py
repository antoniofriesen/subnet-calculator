# stage4.py - Core functions for subnet calculation
# Author: Antonio Friesen

# I. Imports
import math

from utils import (
    ip_to_int,
    int_to_ip,
)


# II. Constants


# III. Helper/Utilities



# calculate_next_power_of_two(hosts: int) -> int
def calculate_next_power_of_two(hosts: int) -> int:
    """Calculates the next power of two"""
    # 1. calculate log2(hosts + 2)  → +2 for network and broadcast
    log_value = math.log2(hosts + 2)

    # 2. round up
    exponent = math.ceil(log_value)

    # 3. return 2^result
    return 2 ** exponent


# IV. Core/Business Logic
# calculate_vlsm(base_network: str, prefix: int, hosts_per_network: list) -> list
def calculate_vlsm(base_network: str, prefix: int, hosts_per_network: list) -> list:
    """Calculates vlsm"""
    # 1. convert base_network to 32-bit integer (current_address)
    base_network_int = ip_to_int(base_network)

    # 2. sort hosts_per_network descending
    sorted_hosts = sorted(hosts_per_network, reverse=True)

    # 3. for each host requirement:
    subnet_list = []

    for host in sorted_hosts:
        # a. calculate next power of two (subnet size)
        subnet_size = calculate_next_power_of_two(host)

        # b. calculate new prefix (32 - log2(subnet_size))
        new_prefix = 32 - int(math.log2(subnet_size))

        # c. calculate new mask
        host_bits = 32 - new_prefix
        if host_bits > 24:
            octet_jump = subnet_size // 16777216
        elif host_bits > 16:
            octet_jump = subnet_size // 65536
        elif host_bits > 8:
            octet_jump = subnet_size // 256
        else:
            octet_jump = subnet_size
        octet = 256 - octet_jump
        if host_bits > 24:
            new_mask = f"{octet}.0.0.0"
        elif host_bits > 16:
            new_mask = f"255.{octet}.0.0"
        elif host_bits > 8:
            new_mask = f"255.255.{octet}.0"
        else:
            new_mask = f"255.255.255.{octet}"

        # d. convert current_address back to ip string
        network_address = int_to_ip(base_network_int)

        # e. append (network_address, mask, max_hosts) to results
        subnet_list.append((network_address, new_mask, subnet_size - 2))

        # f. current_address += subnet_size
        base_network_int += subnet_size

    # 4. return results
    return subnet_list


# V. Input Functions
# get_number_of_networks() -> int
def get_number_of_networks() -> int:
    """Reads the number of networks"""
    while True:
        try:
            # 1. read input "number of networks"
            number_of_networks = int(input("Please enter the number of networks: "))
            # 2. validate: must be >= 1
            if number_of_networks >= 1:
                # 3. return number of networks
                return number_of_networks
            print("Please enter a valid number of networks!")
        except ValueError:
            print("Please enter a valid number of networks!")


# get_hosts_per_network(number_of_networks: int) -> list
def get_hosts_per_network(number_of_networks: int) -> list :
    """Reads the number of hosts per network"""
    # 1. start empty list
    hosts_list = []

    # 2. for each network: read input "hosts for network i"
    for i in range(number_of_networks):
        while True:
            try:
                hosts = int(input(f"Please enter hosts for network {i + 1}: "))
                # 3. validate: must be >= 1
                if hosts >= 1:
                    # 4. append to list
                    hosts_list.append(hosts)
                    break
                print("Must be >= 1!")
            except ValueError:
                print("Please enter a valid number!")
    # 4. return list of hosts
    return hosts_list

# VI. main() - only if needed