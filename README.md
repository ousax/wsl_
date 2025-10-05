# Security Tools Automation Script

This repository provides a Python automation script that installs a full set of security tools, libraries, and terminal customizations for penetration testing and security research environments.
## Features
The script performs the following tasks:
- Installs **Go** (required for many tools).
- Installs **PDTM** (ProjectDiscovery Tool Manager).
- Installs the full suite of **ProjectDiscovery tools** via PDTM.
- Installs a curated set of tools from **tomnomnom**:
  - assetfinder, waybackurls, httprobe, gf, gron, fff, unfurl, anon, meg, comb, qsreplace, bf, html-tool
- Installs **system tools**:  
  - nmap, jq, dirbuster, ffuf
- Installs **Kali Win-KeX**.
- Installs **SecLists**.
- Installs **Python packages**:  
  `requests`, `bs4`, `rich`, `flask`, `matplotlib`, `pandas`, `numpy`, `tqdm`
- Sets **zsh** as the default shell.
- Modifies `~/.zshrc` to include useful aliases.
## Requirements
- WSL [Install wsl](https://learn.microsoft.com/en-us/windows/wsl/install)
- Python 3.x installed.
- Sudo privileges for system-wide installations.
- Internet connection.
## Installation
Clone this repository and make the script executable:
```bash
git clone https://github.com/ousax/wsl_.git
cd wsl_
chmod +x wsl_.py
