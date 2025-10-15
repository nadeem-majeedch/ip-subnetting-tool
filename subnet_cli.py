#!/usr/bin/env python3
"""
Subnetting CLI Tool
Author: Dr. Nadeem Majeed
GitHub: https://github.com/nadeem-majeedch
Email: nadeem.majeed@pucit.edu.pk

A command-line subnetting tool that calculates and displays:
- Network Address
- First Usable IP
- Last Usable IP
- Broadcast Address
- Total Usable Hosts

Usage:
    python subnet_cli.py
"""

import ipaddress
import math
import sys

def subnet_by_number_of_subnets(network, num_subnets):
    """Return a list of subnets by dividing network into `num_subnets`."""
    bits_needed = math.ceil(math.log2(num_subnets))
    new_prefix = network.prefixlen + bits_needed
    if new_prefix > 32:
        raise ValueError("Too many subnets for the given network.")
    return list(network.subnets(new_prefix=new_prefix))

def subnet_by_number_of_hosts(network, num_hosts):
    """Return a list of subnets with enough hosts for `num_hosts` per subnet."""
    bits_needed = math.ceil(math.log2(num_hosts + 2))  # +2 for network and broadcast
    new_prefix = 32 - bits_needed
    if new_prefix < network.prefixlen:
        raise ValueError("Not enough host bits for the given network.")
    return list(network.subnets(new_prefix=new_prefix))

def print_table(subnets):
    """Pretty-print subnetting result in a table format."""
    print("\n{:<8} {:<18} {:<18} {:<18} {:<18} {:<10}".format(
        "Subnet", "Network Address", "First IP", "Last IP", "Broadcast", "Hosts"
    ))
    print("-" * 90)
    for i, subnet in enumerate(subnets, start=1):
        hosts = list(subnet.hosts())
        if hosts:
            first_ip = hosts[0]
            last_ip = hosts[-1]
            total_hosts = subnet.num_addresses - 2
        else:
            first_ip = last_ip = "N/A"
            total_hosts = 0
        print("{:<8} {:<18} {:<18} {:<18} {:<18} {:<10}".format(
            i, str(subnet.network_address), str(first_ip),
            str(last_ip), str(subnet.broadcast_address), total_hosts
        ))
    print("-" * 90)
    print(f"Total subnets: {len(subnets)}\n")

def main():
    print("\n🕸️ Network Subnetting CLI Tool")
    print("Author: Dr. Nadeem Majeed")
    print("-------------------------------------------\n")

    # Get network input
    try:
        network_input = input("Enter network (e.g. 192.168.1.0/24): ").strip()
        network = ipaddress.ip_network(network_input, strict=False)
    except ValueError as e:
        print(f"❌ Invalid network: {e}")
        sys.exit(1)

    # Choose mode
    choice = input("Subnet by (1) Number of Subnets or (2) Number of Hosts? [1/2]: ").strip()
    if choice not in ("1", "2"):
        print("❌ Invalid choice.")
        sys.exit(1)

    try:
        number = int(input("Enter number: ").strip())
        if number <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid number.")
        sys.exit(1)

    # Calculate subnets
    try:
        if choice == "1":
            subnets = subnet_by_number_of_subnets(network, number)
        else:
            subnets = subnet_by_number_of_hosts(network, number)

        print_table(subnets)

    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
