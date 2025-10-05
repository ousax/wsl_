#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    if description:
        print(f"{description}...")
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_installed(tool):
    """Check if a tool is already installed"""
    return shutil.which(tool) is not None

def install_go():
    if check_installed("go"):
        print("Go is already installed")
        return True
    
    print("Installing Go...")
    go_install_cmds = [
        "wget https://golang.org/dl/go1.21.0.linux-amd64.tar.gz",
        "sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz",
        "rm go1.21.0.linux-amd64.tar.gz"
    ]
    
    for cmd in go_install_cmds:
        if not run_command(cmd):
            return False
    go_path = "/usr/local/go/bin"
    os.environ["PATH"] = f"{go_path}:{os.environ['PATH']}"
    
    zshrc_path = Path.home() / ".zshrc"
    go_path_line = f'export PATH="$PATH:{go_path}"\n'
    
    if zshrc_path.exists():
        with open(zshrc_path, 'r') as f:
            content = f.read()
        
        if go_path not in content:
            with open(zshrc_path, 'a') as f:
                f.write(f"\n# Go Lang Path\n{go_path_line}")
    else:
        with open(zshrc_path, 'w') as f:
            f.write(f"# Go Lang Path\n{go_path_line}")
    
    return True

def install_pdtm():
    if check_installed("pdtm"):
        print("PDTM is already installed")
        return True
    
    print("Installing PDTM...")
    return run_command("go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest", "Installing PDTM")

def install_projectdiscovery_tools():
    """Install all projectdiscovery tools using pdtm"""
    print("Installing ProjectDiscovery tools...")
    return run_command("pdtm -ia", "Installing all ProjectDiscovery tools")

def install_tomnomnom_tools():
    print("Installing tomnomnom tools...")
    
    tomnomnom_tools = [
        "github.com/tomnomnom/assetfinder@latest",
        "github.com/tomnomnom/waybackurls@latest",
        "github.com/tomnomnom/httprobe@latest",
        "github.com/tomnomnom/gf@latest",
        "github.com/tomnomnom/gron@latest",
        "github.com/tomnomnom/fff@latest",
        "github.com/tomnomnom/unfurl@latest",
        "github.com/tomnomnom/anon@latest",
        "github.com/tomnomnom/meg@latest",
        "github.com/tomnomnom/comb@latest",
        "github.com/tomnomnom/qsreplace@latest",
        "github.com/tomnomnom/hacks/bf@latest",
        "github.com/tomnomnom/hacks/html-tool@latest",
    ]
    
    success_count = 0
    for tool in tomnomnom_tools:
        if run_command(f"go install -v {tool}", f"Installing {tool.split('/')[-1]}"):
            success_count += 1
    
    print(f"Installed {success_count}/{len(tomnomnom_tools)} tomnomnom tools")
    return success_count > 0

def install_system_tools():
    print("Installing system tools...")
    
    tools = ["nmap", "jq", "dirb", "ffuf"]
    install_cmd = "sudo apt update && sudo apt install -y"
    
    for tool in tools:
        install_cmd += f" {tool}"
    
    return run_command(install_cmd, "Installing system tools")

def install_kex():
    """Install Kali Linux Win-KeX"""
    print("Installing Kali Win-KeX...")
    return run_command("sudo apt install -y kali-win-kex", "Installing Kali Win-KeX")

def install_seclists():
    print("Installing SecLists...")
    return run_command("sudo apt install -y seclists", "Installing SecLists")

def install_python_packages():
    print("Installing Python packages...")
    
    packages = [
        "requests", "bs4", "rich", "flask", 
        "matplotlib", "pandas", "numpy", "tqdm"
    ]
    
    pip_cmd = "pip install --break-system-packages"
    for package in packages:
        pip_cmd += f" {package}"
    
    return run_command(pip_cmd, "Installing Python packages")

def set_default_shell():
    print("Setting zsh as default shell...")
    return run_command('chsh -s $(which zsh)', "Setting zsh as default shell")
    # needs to source it 

def modify_zshrc_aliases():
    """Add aliases to .zshrc file"""
    print("Modifying .zshrc with aliases...")
    
    zshrc_path = Path.home() / ".zshrc"
    
    aliases = [
        "# Custom Aliases",
        'alias linux="kex --win -s"',
        'alias slinux="kex --stop"',
        'alias edit="notepad.exe"',
        'alias edits="notepad.exe"',
        'alias py="python3"',
        'alias pyton="python3"',
        'alias python="python3"',
        'alias pip="pip install --break-system-packages"',
        ""
    ]
    
    # Read existing content
    existing_content = ""
    if zshrc_path.exists():
        with open(zshrc_path, 'r') as f:
            existing_content = f.read()
    
    # Remove existing aliases if they exist
    lines = existing_content.split('\n')
    filtered_lines = []
    skip_next = False
    
    for line in lines:
        if line.startswith("# Custom Aliases"):
            skip_next = True
            continue
        if skip_next and (line.startswith("alias ") or line.startswith("#")):
            continue
        if skip_next and line == "":
            skip_next = False
            continue
        if not skip_next:
            filtered_lines.append(line)
    
    # Add new aliases
    new_content = '\n'.join(filtered_lines).rstrip() + '\n\n' + '\n'.join(aliases)
    
    # Write back to file
    with open(zshrc_path, 'w') as f:
        f.write(new_content)
    
    print("Successfully updated .zshrc with aliases")
    return True

def main():
    """Main function to run all installation tasks"""
    print("Starting automation script...")
    print("=" * 50)
    
    # Check if running as root for some operations
    if os.geteuid() != 0:
        print("Warning: Some operations may require sudo privileges")
    
    tasks = [
        ("Installing Go language", install_go),
        ("Installing PDTM", install_pdtm),
        ("Installing ProjectDiscovery tools", install_projectdiscovery_tools),
        ("Installing tomnomnom tools", install_tomnomnom_tools),
        ("Installing system tools", install_system_tools),
        ("Installing Kali Win-KeX", install_kex),
        ("Installing SecLists", install_seclists),
        ("Installing Python packages", install_python_packages),
        ("Setting zsh as default shell", set_default_shell),
        ("Modifying .zshrc aliases", modify_zshrc_aliases),
    ]
    
    failed_tasks = []
    
    for task_name, task_func in tasks:
        print(f"\n{task_name}")
        print("-" * len(task_name))
        if not task_func():
            failed_tasks.append(task_name)
        print("")
    
    print("=" * 50)
    print("Automation script completed!")
    
    if failed_tasks:
        print(f"Failed tasks: {', '.join(failed_tasks)}")
        print("Please check the errors above and run the script again.")
    else:
        print("All tasks completed successfully!")
        print("Please restart your terminal or run 'source ~/.zshrc' to apply changes.")
    
    return 0 if not failed_tasks else 1

if __name__ == "__main__":
    sys.exit(main())
