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
