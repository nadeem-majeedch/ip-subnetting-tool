import ipaddress
import math
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Subnet Calculation Logic ----------
def subnet_by_number_of_subnets(network, num_subnets):
    bits_needed = math.ceil(math.log2(num_subnets))
    new_prefix = network.prefixlen + bits_needed
    if new_prefix > 32:
        raise ValueError("Too many subnets for the given network.")
    return list(network.subnets(new_prefix=new_prefix))

def subnet_by_number_of_hosts(network, num_hosts):
    bits_needed = math.ceil(math.log2(num_hosts + 2))
    new_prefix = 32 - bits_needed
    if new_prefix < network.prefixlen:
        raise ValueError("Not enough host bits for the given network.")
    return list(network.subnets(new_prefix=new_prefix))

# ---------- GUI Logic ----------
class SubnettingTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🕸️ Advanced Network Subnetting Tool")
        self.geometry("950x500")
        self.minsize(850, 400)
        self.configure(bg="#f4f6f7")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TLabel", background="#f4f6f7", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"))

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = ttk.Label(self, text="🕸️ Network Subnetting Calculator", style="Header.TLabel")
        header.pack(pady=10)

        # Input frame
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Enter Network (e.g. 192.168.1.0/24):").grid(row=0, column=0, sticky="w")
        self.network_entry = ttk.Entry(input_frame, width=30)
        self.network_entry.grid(row=0, column=1, padx=5)

        # Choice between subnet or hosts
        self.choice_var = tk.StringVar(value="subnets")
        ttk.Radiobutton(input_frame, text="By Number of Subnets", variable=self.choice_var, value="subnets").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Radiobutton(input_frame, text="By Number of Hosts", variable=self.choice_var, value="hosts").grid(row=1, column=1, sticky="w", pady=5)

        # Number entry
        ttk.Label(input_frame, text="Enter Number:").grid(row=2, column=0, sticky="w")
        self.number_entry = ttk.Entry(input_frame, width=15)
        self.number_entry.grid(row=2, column=1, sticky="w")

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Calculate", command=self.calculate_subnets).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_results).pack(side="left", padx=5)

        # Result table
        self.tree = ttk.Treeview(self, columns=("Subnet", "Network", "First IP", "Last IP", "Broadcast", "Hosts"), show="headings", height=12)
        for col in ("Subnet", "Network", "First IP", "Last IP", "Broadcast", "Hosts"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0))
        vsb.pack(side="right", fill="y")

    def calculate_subnets(self):
        network_input = self.network_entry.get().strip()
        number_input = self.number_entry.get().strip()

        if not network_input:
            messagebox.showerror("Input Error", "Please enter a valid network.")
            return

        if not number_input.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid number.")
            return

        try:
            network = ipaddress.ip_network(network_input, strict=False)
            number = int(number_input)

            if self.choice_var.get() == "subnets":
                subnets = subnet_by_number_of_subnets(network, number)
            else:
                subnets = subnet_by_number_of_hosts(network, number)

            self.populate_table(subnets)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def populate_table(self, subnets):
        self.clear_results()
        for i, subnet in enumerate(subnets, start=1):
            hosts = list(subnet.hosts())
            if hosts:
                first_ip = hosts[0]
                last_ip = hosts[-1]
                total_hosts = subnet.num_addresses - 2
            else:
                first_ip = last_ip = "N/A"
                total_hosts = 0
            self.tree.insert("", "end", values=(
                i,
                str(subnet.network_address),
                str(first_ip),
                str(last_ip),
                str(subnet.broadcast_address),
                total_hosts
            ))

    def clear_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

# ---------- Run the App ----------
if __name__ == "__main__":
    app = SubnettingTool()
    app.mainloop()
