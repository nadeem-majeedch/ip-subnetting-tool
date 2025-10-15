import ipaddress
import math

def subnet_calculator():
    ip_input = input("Enter IP address (CIDR optional, e.g., 192.168.1.0 or 192.168.1.0/24): ").strip()
    # Auto append /24 if CIDR not provided
    if "/" not in ip_input:
        ip_input += "/24"

    try:
        network = ipaddress.IPv4Network(ip_input, strict=False)
    except ValueError:
        print("❌ Invalid IP or CIDR notation.")
        return

    print("\nChoose mode:")
    print("1. Divide by Number of Subnets")
    print("2. Divide by Number of Hosts per Subnet")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        try:
            num_subnets = int(input("Enter number of subnets: "))
            if num_subnets <= 0:
                raise ValueError
        except ValueError:
            print("❌ Invalid number of subnets.")
            return

        required_bits = (num_subnets - 1).bit_length()
        new_prefix = network.prefixlen + required_bits

    elif choice == "2":
        try:
            hosts_per_subnet = int(input("Enter number of hosts per subnet: "))
            if hosts_per_subnet <= 0:
                raise ValueError
        except ValueError:
            print("❌ Invalid number of hosts.")
            return

        needed_hosts = hosts_per_subnet + 2  # network & broadcast
        required_bits = math.ceil(math.log2(needed_hosts))
        new_prefix = 32 - required_bits

    else:
        print("❌ Invalid choice.")
        return

    # Validation
    if new_prefix > 30:
        print("❌ Too many subnets or too few hosts per subnet.")
        return
    if new_prefix < network.prefixlen:
        print("❌ Cannot allocate requested hosts/subnets within this network.")
        return

    subnets = list(network.subnets(new_prefix=new_prefix))

    print("\n{:<20}{:<18}{:<18}{:<18}{:<18}{:<10}".format(
        "Network", "Subnet Mask", "Broadcast", "First Host", "Last Host", "Hosts"
    ))
    print("-" * 100)

    for subnet in subnets:
        hosts = list(subnet.hosts())
        first_host = hosts[0] if hosts else "-"
        last_host = hosts[-1] if hosts else "-"
        print("{:<20}{:<18}{:<18}{:<18}{:<18}{:<10}".format(
            str(subnet.network_address),
            str(subnet.netmask),
            str(subnet.broadcast_address),
            str(first_host),
            str(last_host),
            len(hosts)
        ))

if __name__ == "__main__":
    subnet_calculator()
