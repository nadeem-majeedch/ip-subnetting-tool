import ipaddress
import math
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

results_cache = []

def calculate_subnets():
    global results_cache
    results_cache = []

    ip_input = ip_entry.get().strip()
    # If user enters plain IP, auto-append /24
    if "/" not in ip_input:
        ip_input += "/24"

    try:
        network = ipaddress.IPv4Network(ip_input, strict=False)
    except ValueError:
        messagebox.showerror("Invalid Input", "❌ Please enter a valid IP address (e.g., 192.168.1.0/24)")
        return

    mode = mode_var.get()
    value = value_entry.get().strip()

    if not value.isdigit() or int(value) <= 0:
        messagebox.showerror("Invalid Input", "❌ Please enter a valid positive number.")
        return

    value = int(value)

    # Determine new prefix based on mode
    if mode == "subnets":
        required_bits = (value - 1).bit_length()
        new_prefix = network.prefixlen + required_bits
    else:  # hosts mode
        needed_hosts = value + 2  # account for network and broadcast
        required_bits = math.ceil(math.log2(needed_hosts))
        new_prefix = 32 - required_bits

    if new_prefix > 30:
        messagebox.showerror("Error", "❌ Too many subnets or too few hosts per subnet.")
        return
    if new_prefix < network.prefixlen:
        messagebox.showerror("Error", "❌ Cannot allocate requested hosts/subnets within this network.")
        return

    # Clear previous results
    for row in tree.get_children():
        tree.delete(row)

    # Calculate and display subnets
    subnets = list(network.subnets(new_prefix=new_prefix))
    for subnet in subnets:
        network_address = subnet.network_address
        broadcast_address = subnet.broadcast_address
        netmask = subnet.netmask
        hosts = list(subnet.hosts())
        first_host = hosts[0] if hosts else "-"
        last_host = hosts[-1] if hosts else "-"
        total_hosts = len(hosts)

        data = (
            str(network_address),
            str(netmask),
            str(broadcast_address),
            str(first_host),
            str(last_host),
            str(total_hosts)
        )
        results_cache.append(data)
        tree.insert("", "end", values=data)

def export_to_csv():
    if not results_cache:
        messagebox.showinfo("No Data", "⚠️ Please calculate subnets before exporting.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save subnet information"
    )
    if not file_path:
        return

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Network Address", "Subnet Mask", "Broadcast", "First Host", "Last Host", "Total Hosts"])
        for row in results_cache:
            writer.writerow(row)

    messagebox.showinfo("Export Successful", f"✅ Subnet data exported to:\n{file_path}")

# GUI Setup
root = tk.Tk()
root.title("🌐 Advanced IP Subnet Calculator — by Dr. Nadeem Majeed")
root.geometry("1050x600")
root.resizable(False, False)

frame = ttk.Frame(root, padding="10")
frame.pack(fill="x")

# IP Entry
ttk.Label(frame, text="Enter IP Address (CIDR):").grid(column=0, row=0, padx=5, pady=5)
ip_entry = ttk.Entry(frame, width=25)
ip_entry.grid(column=1, row=0, padx=5, pady=5)
ip_entry.insert(0, "192.168.1.0/24")

# Mode selection
mode_var = tk.StringVar(value="subnets")
ttk.Radiobutton(frame, text="Number of Subnets", variable=mode_var, value="subnets").grid(column=2, row=0, padx=5, pady=5)
ttk.Radiobutton(frame, text="Number of Hosts per Subnet", variable=mode_var, value="hosts").grid(column=3, row=0, padx=5, pady=5)

# Value entry
value_entry = ttk.Entry(frame, width=15)
value_entry.grid(column=4, row=0, padx=5, pady=5)
value_entry.insert(0, "4")

# Buttons
ttk.Button(frame, text="Calculate", command=calculate_subnets).grid(column=5, row=0, padx=5, pady=5)
ttk.Button(frame, text="Export CSV", command=export_to_csv).grid(column=6, row=0, padx=5, pady=5)

# Treeview for results
columns = ("Network Address", "Subnet Mask", "Broadcast", "First Host", "Last Host", "Total Hosts")
tree = ttk.Treeview(root, columns=columns, show="headings", height=22)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=160)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# Run App
root.mainloop()
