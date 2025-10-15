# 🕸️ Network Subnetting Tool (GUI + CLI)

An advanced and user-friendly **Python Network Subnetting Tool** that allows users to quickly calculate and view subnet details by providing an IP address and either the number of subnets or hosts.  

This tool is designed for network engineers, students, and IT professionals who need a fast and visual way to calculate subnet ranges without manual math.

---

## ✨ Features

- ✅ **Two calculation modes**:  
  - By number of subnets  
  - By number of hosts
- 🖥️ **Modern GUI using Tkinter** — clean, responsive, and easy to use
- 🧮 Displays:
  - Subnet Number
  - Network Address
  - First IP
  - Last IP
  - Broadcast Address
  - Total Usable Hosts
- 🪄 Error handling for invalid inputs
- 🧰 Standalone `.exe` build for Windows (no Python required)

---

## 🖼️ GUI Preview


| Subnet | Network Address | First IP       | Last IP        | Broadcast      | Hosts |
|--------|-----------------|---------------|---------------|---------------|-------|
| 1      | 192.168.1.0     | 192.168.1.1   | 192.168.1.62  | 192.168.1.63  | 62    |
| 2      | 192.168.1.64    | 192.168.1.65  | 192.168.1.126 | 192.168.1.127 | 62    |
| ...    | ...             | ...           | ...           | ...           | ...   |

---

## 🧑‍💻 Installation (Python Version)

1. Clone this repository:
   ```bash
   git clone https://github.com/nadeem-majeedch/network-subnetting-tool.git
   cd network-subnetting-tool```
2. Install dependencies (only standard library is used, but recommended to create a venv):
```
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```
3. Run the tool:
```
python network_subnet_tool.py
```
## 📂 Project Structure
network-subnetting-tool/
├── network_subnet_tool.py    # Main GUI tool
├── subnet_cli.py             # CLI version
├── requirements.txt
├── README.md
└── icon.ico                  # icon for .exe


## 🧑 Author

Dr. Muhammad Nadeem Majeed

📧 nadeem.majeed@pucit.edu.pk

🌐 GitHub Profile

## 🌟 Support the Project

**If you find this tool helpful, please consider giving the repo a** ⭐ **star to support future development!**
## Subnetting doesn’t have to be hard — make it visual, fast, and fun.


