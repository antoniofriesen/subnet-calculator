# main.py - Entry point for the subnet calculator
# Author: Antonio Friesen

from calculator import get_base_network_ip, calculate_subnets, get_number_of_subnets


def main() -> None:
    """Main function"""
    base_network = get_base_network_ip()
    number_of_subnets = get_number_of_subnets()

    max_hosts, new_mask, subnets = calculate_subnets(base_network, number_of_subnets)

    print(f"\nMaximum hosts per subnet: {max_hosts}")
    print(f"New subnet mask:          {new_mask}")
    print()
    for i, subnet in enumerate(subnets, start=1):
        print(f"  {i}. Network: {subnet}")


if __name__ == "__main__":
    main()