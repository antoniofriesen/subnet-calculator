# stage3.py - Core functions for subnet calculation
# Author: Antonio Friesen


# calculate_subnets_arbitrary(base_network: str, prefix: int, number_of_subnets: int) -> tuple
def calculate_subnets_arbitrary(base_network: str, prefix: int, number_of_subnets: int) -> tuple:
    """Calculates subnets based in the base network, arbitrary prefix and number of subnets"""
    # 2. split base_network into 4 octets
    split_ip = base_network.split(".")

    # 3. calculate total host bits (32 - prefix)
    host_bits = 32 -prefix

    # 4. calculate host bits per octet (4th, 3rd, 2nd, 1st)
    if host_bits >= 24:
        octet_host_bits = max(host_bits - 24, 0)
    elif host_bits >= 16:
        octet_host_bits = min(max(host_bits - 16, 0), 8)
    elif host_bits >= 8:
        octet_host_bits = min(max(host_bits - 8, 0), 8)
    else:
        octet_host_bits = min(host_bits, 8)

    # 5. calculate step per octet (2^octet_host_bits)
    jump = 2 ** (octet_host_bits)

    # 6. calculate total hosts per subnet (2^total_host_bits - 2)
    host_count = 2 ** host_bits - 2

    # 7. calculate new subnet mask
    octet = 256 - jump
    if host_bits > 24:
        new_mask = f"{octet}.0.0.0"
    elif host_bits > 16:
        new_mask = f"255.{octet}.0.0"
    elif host_bits > 8:
        new_mask = f"255.255.{octet}.0"
    else:
        new_mask = f"255.255.255.{octet}"

    # 8. for each subnet: calculate network address using steps
    if host_bits > 24:
        array_subnets = []
        for subnet in range(number_of_subnets):
            array_subnets.append(
                f"{subnet * jump}."
                f"{split_ip[1]}."
                f"{split_ip[2]}."
                f"{split_ip[3]}"
            )
    elif host_bits > 16:
        array_subnets = []
        for subnet in range(number_of_subnets):
            array_subnets.append(
                f"{split_ip[0]}."
                f"{subnet * jump}."
                f"{split_ip[2]}."
                f"{split_ip[3]}"
            )
    elif host_bits > 8:
        array_subnets = []
        for subnet in range(number_of_subnets):
            array_subnets.append(
                f"{split_ip[0]}."
                f"{split_ip[1]}."
                f"{subnet * jump}."
                f"{split_ip[3]}"
            )
    else:
        array_subnets = []
        for subnet in range(number_of_subnets):
            array_subnets.append(
                f"{split_ip[0]}."
                f"{split_ip[1]}."
                f"{split_ip[2]}."
                f"{subnet * jump}"
            )

    # 9. return (max_hosts, new_mask, array_subnets)
    return (host_count, new_mask, array_subnets)


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


def get_number_of_subnets(prefix: int) -> int:
    """Reads the number of desired subnets from the user"""
    while True:
        try:
            number_of_subnets = int(input("Please enter the number of subnets: "))
            if validate_subnets_for_prefix(number_of_subnets, prefix):
                return number_of_subnets
            print("Invalid number of subnets!")
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
    # calculate host bits (32 - prefix)
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


def validate_subnets_for_prefix(number_subnets: int, prefix: int) -> bool:
    """Validates number of subnets for a given prefix"""
    # 1. calculate host bits (32 - prefix)
    host_bits = 32 - prefix

    # 2. calculate host bits in relevant octet
    if host_bits >= 24:
        octet_host_bits = max(host_bits - 24, 0)
    elif host_bits >= 16:
        octet_host_bits = min(max(host_bits - 16, 0), 8)
    elif host_bits >= 8:
        octet_host_bits = min(max(host_bits - 8, 0), 8)
    else:
        octet_host_bits = min(host_bits, 8)

    # 3. calculate max subnets
    jump = 2 ** octet_host_bits
    max_subnets = 256 // jump

    # 4. check if number_subnets <= max_subnets
    if number_subnets > max_subnets:
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
