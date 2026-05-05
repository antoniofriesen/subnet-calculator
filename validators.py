# validators.py - Input validation functions for the subnet calculator
# Author: Antonio Friesen


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