# stage4.py - Core functions for subnet calculation
# Author: Antonio Friesen

# I. Imports
import math


# II. Constants


# III. Helper/Utilities
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


def validate_prefix(prefix: int) -> bool:
    """Validates ip address"""
    # 1. check if prefix is in range 1, 31
    if prefix not in range(1,31):
        return False

    # 2. return True if valid, False otherwise
    return True


def validate_cidr(cidr: str) -> bool:
    """Validates the network CIDR"""
    # 1. trim input
    trimmed_cidr = cidr.strip()

    # 2. check if "/" exists in input
    if "/" not in trimmed_cidr:
        return False

    # 3. split on "/" into ip and prefix parts
    ip, prefix = trimmed_cidr.split("/")
    split_ip = ip.split(".")

    # 4. validate ip part with validate_ip()
    if not validate_ip(ip):
        return False

    # 5. validate prefix part with validate_prefix()
    try:
        if not validate_prefix(int(prefix)):
            return False
    except ValueError:
        return False

    # 6. check if ip matches prefix
    host_bits = 32 - int(prefix)

    # convert each octet to 32-bit integer
    octet1 = int(split_ip[0]) * 16777216
    octet2 = int(split_ip[1]) * 65536
    octet3 = int(split_ip[2]) * 256
    octet4 = int(split_ip[3])
    ip_int = octet1 + octet2 + octet3 + octet4

    # check if last host_bits bits are all 0
    if ip_int % (2 ** host_bits) != 0:
        return False

    # 7. return True if valid, False otherwise
    return True


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
def calculate_vlsm(base_network: str, prefix: int, hosts_per_network: list) ->list:
    """Calculates vlsm"""
    # 1. convert base_network to 32-bit integer (current_address)
    octets = base_network.split(".")
    octet1 = int(octets[0]) * 16777216
    octet2 = int(octets[1]) * 65536
    octet3 = int(octets[2]) * 256
    octet4 = int(octets[3])
    base_network_int = octet1 + octet2 + octet3 + octet4

    # 2. sort hosts_per_network descending
    sorted_hosts = sorted(hosts_per_network, reverse=True)

    # 3. for each host requirement:
    current_address = base_network_int
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
        octet1 = current_address // 16777216
        octet2 = (current_address % 16777216) // 65536
        octet3 = (current_address % 65536) // 256
        octet4 = current_address % 256
        network_address = f"{octet1}.{octet2}.{octet3}.{octet4}"

        # e. append (network_address, mask, max_hosts) to results
        subnet_list.append((network_address, new_mask, subnet_size - 2))

        # f. current_address += subnet_size
        current_address += subnet_size

    # 4. return results
    return subnet_list


# V. Input Functions
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