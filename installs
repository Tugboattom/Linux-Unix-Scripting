#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse  # Added for CLI parameter handling

# Check for root privileges
if os.geteuid() != 0:
    print("This script must be run with sudo privileges.")
    sys.exit(1)

# Update package lists first
subprocess.run(["apt", "update", "-y"], check=True)

# List of software to install
software_list = [
    # (Display Name, Tag, Installation Command)
    ("Visual Studio Code", "vscode", "installation command"),
    ("GIMP", "gimp", "apt install -y gimp"),
    # Add other software entries here...
]

def install_packages(selections):
    """
    Install the selected packages using their respective installation commands.
    """
    for idx in selections:
        name, _, command = software_list[idx - 1]
        print(f"\n\033[1;34mInstalling {name}...\033[0m")
        try:
            subprocess.run(
                command, 
                shell=True, 
                check=True,
                executable="/bin/bash"
            )
            print(f"\033[1;32m{name} installed successfully!\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[1;31mError installing {name}: {e}\033[0m")

def show_menu():
    """
    Display a whiptail checklist for the user to select software to install.
    Returns a list of selected indices (1-based) or None if the user cancels.
    """
    instruction_text = (
        "Navigate: ↑↓ • Select: [Space] • Confirm: [Enter]\n"
        "Multiple selections allowed • Cancel: Esc"
    )
    
    cmd = [
        "whiptail", 
        "--title", "Software Installation (Select with SPACE)",
        "--checklist", 
        instruction_text,
        "--notags",
        "35", "85", "15"
    ]
    
    for idx, (name, tag, _) in enumerate(software_list, 1):
        cmd.extend((str(idx), name, "OFF"))
    
    try:
        result = subprocess.run(
            cmd, 
            stderr=subprocess.PIPE, 
            check=True, 
            text=True
        )
        selected = result.stderr.strip().replace('"', '').split()
        return [int(i) for i in selected]
    except subprocess.CalledProcessError:
        return None

def main():
    """
    Main interactive loop for the script.
    Allows the user to select and install software multiple times.
    """
    while True:
        selections = show_menu()
        if not selections:
            confirm_exit = subprocess.run(
                ["whiptail", "--yesno", "Exit installer?", "7", "40"],
                stderr=subprocess.DEVNULL
            ).returncode
            if confirm_exit == 0:
                break
            continue
        
        install_packages(selections)
        
        continue_install = subprocess.run(
            ["whiptail", "--yesno", "Install more software?", "7", "40"],
            stderr=subprocess.DEVNULL
        ).returncode
        
        if continue_install != 0:
            break

def parse_cli_args():
    """
    Parse CLI arguments to allow direct software installation without the interactive menu.
    """
    parser = argparse.ArgumentParser(
        description="Install software packages interactively or via CLI."
    )
    parser.add_argument(
        "--install",
        nargs="+",
        help="List of software tags to install (e.g., --install vscode gimp)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available software packages and their tags.",
    )
    return parser.parse_args()

def get_indices_from_tags(tags):
    """
    Convert software tags to their corresponding indices in the software_list.
    """
    indices = []
    for tag in tags:
        for idx, (_, software_tag, _) in enumerate(software_list, 1):
            if software_tag == tag:
                indices.append(idx)
                break
        else:
            print(f"\033[1;31mError: Software with tag '{tag}' not found.\033[0m")
            sys.exit(1)
    return indices

def list_software():
    """
    Display all available software packages and their tags.
    """
    print("\033[1;34mAvailable Software:\033[0m")
    for name, tag, _ in software_list:
        print(f"- {name} (\033[1;32m{tag}\033[0m)")

if __name__ == "__main__":
    args = parse_cli_args()

    if args.list:
        # List all available software and exit
        list_software()
        sys.exit(0)

    if args.install:
        # Install software specified via CLI
        selections = get_indices_from_tags(args.install)
        install_packages(selections)
    else:
        # Run the interactive menu
        try:
            main()
            print("\n\033[1;32mInstallation complete!\033[0m")
        except KeyboardInterrupt:
            print("\n\033[1;31mInstallation cancelled!\033[0m")
            sys.exit(1)
