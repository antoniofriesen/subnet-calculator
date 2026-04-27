# main.py - Entry point for the subnet calculator
# Author: Antonio Friesen

from stage1 import (
    get_base_network_ip as get_ip_s1,
    get_number_of_subnets as get_subnets_s1,
    calculate_subnets
)
from stage2 import (
    get_network_cidr as get_network_s2,
    get_number_of_subnets as get_subnets_s2,
    calculate_subnets_extended
)
from stage3 import (
    get_network_cidr as get_network_s3,
    get_number_of_subnets as get_subnets_s3,
    calculate_subnets_arbitrary
)
from stage4 import (
    get_network_cidr as get_network_s4,
    get_number_of_networks,
    get_hosts_per_network,
    calculate_vlsm
)


def main() -> None:
    """Main function"""
    print("=== Subnet Calculator ===")
    print("\nStage 1: Symmetric subnetting for /24 networks")
    print("Stage 2: Extended subnetting for /8, /16 and /24 networks")
    print("Stage 3: Arbitrary prefix subnetting for any prefix (1-30)")
    print("Stage 4: VLSM - Variable Length Subnet Masking")
    stage = int(input("\nChoose a stage (1, 2, 3 or 4): "))

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
        base_network, prefix = get_network_s2()
        number_of_subnets = get_subnets_s2()

        max_hosts, new_mask, subnets = calculate_subnets_extended(base_network, prefix, number_of_subnets)

        print(f"\nMaximum hosts per subnet: {max_hosts}")
        print(f"New subnet mask:          {new_mask}")
        print()
        for i, subnet in enumerate(subnets, start=1):
            print(f"  {i}. Network: {subnet}")
        print("\n--- Calculation complete ---")

    if stage == 3:
        print("\n--- Stage 3: Arbitrary Prefix Subnetting ---")
        base_network, prefix = get_network_s3()
        number_of_subnets = get_subnets_s3(prefix)

        max_hosts, new_mask, subnets = calculate_subnets_arbitrary(base_network, prefix, number_of_subnets)

        print(f"\nMaximum hosts per subnet: {max_hosts}")
        print(f"New subnet mask:          {new_mask}")
        print()
        for i, subnet in enumerate(subnets, start=1):
            print(f"  {i}. Network: {subnet}")
        print("\n--- Calculation complete ---")

    if stage == 4:
        print("\n--- Stage 4: VLSM ---")
        base_network, prefix = get_network_s4()
        number_of_networks = get_number_of_networks()
        hosts_per_network = get_hosts_per_network(number_of_networks)

        subnet_list = calculate_vlsm(base_network, prefix, hosts_per_network)

        print()
        for i, (network_address, new_mask, max_hosts) in enumerate(subnet_list, start=1):
            print(f"  {i}. Network: {network_address}  Mask: {new_mask}  Max Hosts: {max_hosts}")
        print("\n--- Calculation complete ---")


if __name__ == "__main__":
    main()