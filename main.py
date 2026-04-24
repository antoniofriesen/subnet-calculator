# main.py - Entry point for the subnet calculator
# Author: Antonio Friesen

from stage1 import (
    get_base_network_ip as get_ip_s1,
    get_number_of_subnets as get_subnets_s1,
    calculate_subnets
)
from stage2 import (
    get_number_of_subnets as get_subnets_s2,
    calculate_subnets_extended,
    get_network_cidr,
)


def main() -> None:
    """Main function"""
    print("=== Subnet Calculator ===")
    print("\nStage 1: Symmetric subnetting for /24 networks")
    print("Stage 2: Extended subnetting for /8, /16 and /24 networks")
    stage = int(input("\nChoose a stage (1 or 2): "))

    if stage == 1:
        print("\n--- Stage 1: Symmetric Subnetting ---")
        base_network = get_ip_s1()
        number_of_subnets = get_subnets_s1()

        max_hosts, new_mask, subnets = calculate_subnets(base_network, number_of_subnets)

        print(f"\nMaximum hosts per subnet: {max_hosts}")
        print(f"New subnet mask:          {new_mask}")
        print()
        for i, subnet in enumerate(subnets, start=1):
            print(f"  {i}. Network: {subnet}")
        print("\n--- Calculation complete ---")

    if stage == 2:
        print("\n--- Stage 2: Extended Subnetting ---")
        base_network, prefix = get_network_cidr()
        number_of_subnets = get_subnets_s2()

        max_hosts, new_mask, subnets = calculate_subnets_extended(base_network, prefix, number_of_subnets)

        print(f"\nMaximum hosts per subnet: {max_hosts}")
        print(f"New subnet mask:          {new_mask}")
        print()
        for i, subnet in enumerate(subnets, start=1):
            print(f"  {i}. Network: {subnet}")
        print("\n--- Calculation complete ---")


if __name__ == "__main__":
    main()