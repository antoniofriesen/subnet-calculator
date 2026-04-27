# Subnet Calculator

A command-line tool for IPv4 subnet calculation, built without the use of any subnetting libraries (e.g. `ipaddress`). All logic is implemented manually using bit-level arithmetic.

## Features

### Stage 1 – Symmetric Subnetting (/24)
- Input: base network (`/24`) + number of desired subnets
- Output: network addresses, subnet mask, and maximum hosts per subnet

### Stage 2 – Extended Subnetting (/8, /16, /24)
- Input: base network in CIDR format + number of desired subnets
- Output: network addresses, subnet mask, and maximum hosts per subnet
- Includes input validation with meaningful error messages

### Stage 3 – Arbitrary Prefix Subnetting (1–30)
- Input: base network in CIDR format + number of desired subnets
- Supports any prefix from `/1` to `/30`
- Output: network addresses, subnet mask, and maximum hosts per subnet
- Validates that the number of subnets fits within the given prefix

### Stage 4 – VLSM (Variable Length Subnet Masking)
- Input: base network in CIDR format + number of networks + hosts per network
- Automatically sorts networks by size (largest first)
- Output: network address, subnet mask, and maximum hosts for each subnet

## Project Structure

```
subnet-calculator/
├── main.py      # Entry point
├── stage1.py    # Stage 1 functions
├── stage2.py    # Stage 2 functions
├── stage3.py    # Stage 3 functions
└── stage4.py    # Stage 4 functions
```

## Usage

```bash
python main.py
```

Follow the on-screen prompts to choose a stage and enter the required inputs.

## Example – Stage 4 (VLSM)

```
Base network: 192.168.1.0/24
Number of networks: 3
Hosts for network 1: 100
Hosts for network 2: 50
Hosts for network 3: 10

1. Network: 192.168.1.0    Mask: 255.255.255.128  Max Hosts: 126
2. Network: 192.168.1.128  Mask: 255.255.255.192  Max Hosts: 62
3. Network: 192.168.1.192  Mask: 255.255.255.240  Max Hosts: 14
```

## Requirements

- Python 3.8+
- No external libraries required

## Author

Antonio Friesen