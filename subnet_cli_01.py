import ipaddress

def subnet_calculator():
    ip_input = input("Enter IP address with CIDR (e.g., 192.168.1.0/24): ")
    try:
        network = ipaddress.IPv4Network(ip_input, strict=False)
    except ValueError:
        print("❌ Invalid IP or CIDR notation.")
        return

    try:
        num_subnets = int(input("Enter number of subnets: "))
        if num_subnets <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid number of subnets.")
        return

    required_bits = (num_subnets - 1).bit_length()
    new_prefix = network.prefixlen + required_bits

    if new_prefix > 30:
        print("❌ Too many subnets. Subnet mask would be too small.")
        return

    subnets = list(network.subnets(new_prefix=new_prefix))

    print(f"\n{'Subnet':<20}{'Subnet Mask':<18}{'Broadcast':<18}{'First Host':<18}{'Last Host':<18}{'Hosts'}")
    print("-" * 90)
    for subnet in subnets:
        hosts = list(subnet.hosts())
        first_host = hosts[0] if hosts else "-"
        last_host = hosts[-1] if hosts else "-"
        print(f"{str(subnet.network_address):<20}{str(subnet.netmask):<18}{str(subnet.broadcast_address):<18}{str(first_host):<18}{str(last_host):<18}{len(hosts)}")

if __name__ == "__main__":
    subnet_calculator()
