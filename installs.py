#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse

# Check for root privileges
if os.geteuid() != 0:
    print("This script must be run with sudo privileges.")
    sys.exit(1)

# Update package lists first
subprocess.run(["apt", "update", "-y"], check=True)

# List of software to install
software_list = [
    # (Display Name, Tag, Installation Command)
    ("Visual Studio Code", "vscode",
     "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg; "
     "install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/; "
     "echo 'deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] "
     "https://packages.microsoft.com/repos/vscode stable main' > /etc/apt/sources.list.d/vscode.list; "
     "apt update -y; apt install -y code; rm packages.microsoft.gpg"),
    
    ("GIMP", "gimp", 
     "apt install -y gimp"),
    
    ("Blender", "blender", 
     "apt install -y blender"),
    
    ("OBS Studio", "obs-studio", 
     "apt install -y obs-studio"),
    
    ("Gnome Tweaks", "gnome-tweaks", 
     "apt install -y gnome-tweaks"),
    
    ("VLC", "vlc", 
     "apt install -y vlc"),
    
    ("Node.js", "nodejs", 
     "curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -; apt install -y nodejs"),
    
    ("MongoDB Server", "mongodb-server", 
     "wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/mongodb.gpg; "
     "echo 'deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse' > /etc/apt/sources.list.d/mongodb-org-6.0.list; "
     "apt update -y; apt install -y mongodb-org; systemctl enable mongod; systemctl start mongod"),
    
    ("MongoDB Compass", "mongodb-compass", 
     "wget https://downloads.mongodb.com/compass/mongodb-compass_1.35.0_amd64.deb; "
     "dpkg -i mongodb-compass_1.35.0_amd64.deb; apt install -f -y; rm mongodb-compass_1.35.0_amd64.deb"),
    
    ("Figma", "figma", 
     "wget https://www.figma.com/download/desktop/linux -O figma.deb; "
     "dpkg -i figma.deb; apt install -f -y; rm figma.deb"),
    
    ("Enpass", "enpass", 
     "echo 'deb https://apt.enpass.io/ stable main' > /etc/apt/sources.list.d/enpass.list; "
     "wget -O - https://apt.enpass.io/keys/enpass-linux.key | gpg --dearmor > /etc/apt/trusted.gpg.d/enpass.gpg; "
     "apt update -y; apt install -y enpass"),
    
    ("Chromium", "chromium", 
     "apt install -y chromium-browser"),
    
    ("Inkscape", "inkscape", 
     "apt install -y inkscape"),
    
    ("X-Mind", "xmind", 
     "wget https://www.xmind.net/xmind/downloads/xmind-2021-11-22-amd64.deb; "
     "dpkg -i xmind-2021-11-22-amd64.deb; apt install -f -y; rm xmind-2021-11-22-amd64.deb"),
    
    ("Discord", "discord", 
     "wget -O discord.deb 'https://discord.com/api/download?platform=linux&format=deb'; "
     "dpkg -i discord.deb; apt install -f -y; rm discord.deb"),
    
    ("CIFS Utils", "cifs-utils", 
     "apt install -y cifs-utils"),
    
    ("Wine", "wine", 
     "dpkg --add-architecture i386; "
     "wget -qO- https://dl.winehq.org/wine-builds/winehq.key | gpg --dearmor > /etc/apt/trusted.gpg.d/winehq.gpg; "
     "echo 'deb https://dl.winehq.org/wine-builds/ubuntu/ $(lsb_release -cs) main' > /etc/apt/sources.list.d/winehq.list; "
     "apt update -y; apt install -y --install-recommends winehq-stable"),
    
    ("Zoom", "zoom", 
     "wget https://zoom.us/client/latest/zoom_amd64.deb; "
     "dpkg -i zoom_amd64.deb; apt install -f -y; rm zoom_amd64.deb"),
    
    ("Git", "git", 
     "apt install -y git"),
    
    ("Putty", "putty", 
     "apt install -y putty"),
    
    ("Curl", "curl", 
     "apt install -y curl"),
    
    ("Docker", "docker", 
     "install -m 0755 -d /etc/apt/keyrings; "
     "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg; "
     "chmod a+r /etc/apt/keyrings/docker.gpg; "
     "echo 'deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] "
     "https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable' | "
     "tee /etc/apt/sources.list.d/docker.list > /dev/null; "
     "apt update -y; apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"),
    
    ("PostgreSQL", "postgresql", 
     "apt install -y postgresql"),
    
    ("Golang", "golang", 
     "apt install -y golang-go"),
    
    ("Spotify", "spotify", 
     "curl -sS https://download.spotify.com/debian/pubkey_7A3A762FAFD4A51F.gpg | gpg --dearmor > /etc/apt/trusted.gpg.d/spotify.gpg; "
     "echo 'deb http://repository.spotify.com stable non-free' > /etc/apt/sources.list.d/spotify.list; "
     "apt update -y; apt install -y spotify-client"),
    
    ("Postman", "postman", 
     "wget https://dl.pstmn.io/download/latest/linux_64 -O postman.tar.gz; "
     "tar -xzf postman.tar.gz -C /opt; ln -s /opt/Postman/Postman /usr/bin/postman; rm postman.tar.gz")
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
