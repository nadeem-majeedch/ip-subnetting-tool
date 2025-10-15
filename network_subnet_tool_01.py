import ipaddress
import math
import tkinter as tk
from tkinter import ttk, messagebox

def calculate_subnets():
    ip_input = ip_entry.get().strip()
    try:
        network = ipaddress.IPv4Network(ip_input, strict=False)
    except ValueError:
        messagebox.showerror("Invalid Input", "❌ Please enter a valid IP address with CIDR (e.g., 192.168.1.0/24)")
        return

    mode = mode_var.get()
    value = value_entry.get().strip()

    if not value.isdigit() or int(value) <= 0:
        messagebox.showerror("Invalid Input", "❌ Please enter a valid positive number.")
        return

    value = int(value)

    # Determine new prefix based on selected mode
    if mode == "subnets":
        required_bits = (value - 1).bit_length()
        new_prefix = network.prefixlen + required_bits
    else:  # mode == "hosts"
        # Include network & broadcast, so add 2
        needed_hosts = value + 2
        required_bits = math.ceil(math.log2(needed_hosts))
        new_prefix = 32 - required_bits

    # Validation
    if new_prefix > 30:
        messagebox.showerror("Error", "❌ Too many subnets or too few hosts per subnet.")
        return
    if new_prefix < network.prefixlen:
        messagebox.showerror("Error", "❌ Cannot allocate requested hosts/subnets within this network.")
        return

    # Clear previous results
    for row in tree.get_children():
        tree.delete(row)

    # Calculate and display
    subnets = list(network.subnets(new_prefix=new_prefix))
    for subnet in subnets:
        network_address = subnet.network_address
        broadcast_address = subnet.broadcast_address
        netmask = subnet.netmask
        hosts = list(subnet.hosts())
        first_host = hosts[0] if hosts else "-"
        last_host = hosts[-1] if hosts else "-"
        total_hosts = len(hosts)
        tree.insert("", "end", values=(
            str(network_address),
            str(netmask),
            str(broadcast_address),
            str(first_host),
            str(last_host),
            str(total_hosts)
        ))

# GUI setup
root = tk.Tk()
root.title("💻 Advanced IP Subnet Calculator — by Dr. Nadeem Majeed")
root.geometry("1000x550")
root.resizable(False, False)

frame = ttk.Frame(root, padding="10")
frame.pack(fill="x")

ttk.Label(frame, text="Enter IP Address (CIDR):").grid(column=0, row=0, padx=5, pady=5)
ip_entry = ttk.Entry(frame, width=25)
ip_entry.grid(column=1, row=0, padx=5, pady=5)
ip_entry.insert(0, "192.168.1.0/24")

# Mode selection
mode_var = tk.StringVar(value="subnets")
ttk.Radiobutton(frame, text="Number of Subnets", variable=mode_var, value="subnets").grid(column=2, row=0, padx=5, pady=5)
ttk.Radiobutton(frame, text="Number of Hosts per Subnet", variable=mode_var, value="hosts").grid(column=3, row=0, padx=5, pady=5)

value_entry = ttk.Entry(frame, width=15)
value_entry.grid(column=4, row=0, padx=5, pady=5)
value_entry.insert(0, "4")

ttk.Button(frame, text="Calculate", command=calculate_subnets).grid(column=5, row=0, padx=5, pady=5)

# Treeview for results
columns = ("Network Address", "Subnet Mask", "Broadcast", "First Host", "Last Host", "Total Hosts")
tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
