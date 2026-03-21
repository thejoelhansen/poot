#!/usr/bin/env python3


# --- Main !TODO 
# Make non sudo install path into user's home directory: Updating all paths to install $HOME/.app_name/ if ran without sudo (IE python3 install.py)


# Library imports
import sys
import subprocess
import shutil
import glob
from pathlib import Path
import configparser

# App name
# Load config
config = configparser.ConfigParser()
config.read("config.ini")

# Get app name from config
app_name = config.get("APP", "app_name")

# Check if Python version > 3.9
def check_python_version(min_version=(3, 9)):

    # Get Python version string
    version_string = subprocess.run(
        ["python3", "--version"], 
        check=True, 
        capture_output=True, 
        text=True
    )

    # Convert version string to number
    version_list = version_string.stdout.split()[1]
    version_tuple_string = tuple(version_list.split("."))
    version_number = tuple(map(int, version_tuple_string))
    
    # Compare current installed version with minimum version 
    version_is_greater = version_number >= min_version
 
    return version_is_greater

# Guardrail: Fail if Python version is < 3.9
if __name__ == "__main__":
    version_check = check_python_version()
    
    if version_check == True:
        print(f"[{app_name}] Success! Python minimum version is at least 3.9")
    else:
        print(f"[{app_name}] Exiting installation: Python must be at least 3.9")
        exit(1)

# Create folders
def create_dirs(dir_list):
    for directory in dir_list:
        print(f"[{app_name}] Creating {directory}")
        subprocess.run(["mkdir", "-p", directory], check=True)

create_dirs([
    f"/usr/local/lib/{app_name}/runners",
    f"/usr/local/lib/{app_name}/commands"
])

# Copy files to default global install directory
def copy_file(source_file, destination_folder):
    for file in glob.glob(source_file): 
        print(f"[{app_name}] Copying {file}")
        shutil.copy(file, destination_folder)

# Copy executable
copy_file(f"./{app_name}.py", f"/usr/local/bin/{app_name}")
# Copy core files
copy_file("./runners/*", f"/usr/local/lib/{app_name}/runners/")
copy_file("./README.md", f"/usr/local/lib/{app_name}/")
copy_file("./install.py", f"/usr/local/lib/{app_name}/")
copy_file("./commands/*", f"/usr/local/lib/{app_name}/commands/")

# Verify install

# Collection missing files
missing = []

# TODO add required runners & commands to config for customizable install requirements

required_files = [
    f"/usr/local/bin/{app_name}",
    f"/usr/local/lib/{app_name}/runners/shell.py",
    f"/usr/local/lib/{app_name}/commands",
    f"/usr/local/lib/{app_name}/install.py"
]

# Check if required files exist, appending the missing files to missing[]
for path in required_files:
    if not Path(path).exists():
        missing.append(path)

# See if anything was added to missing[]
if missing:
    print(f"[{app_name}] Failed to install:")
    for file in missing:
        print(f"- {file}")
        print("Exiting installation:")
        exit(1)

# Update executable permissions

try:
    subprocess.run(
        ["chmod", "755", f"/usr/local/bin/{app_name}"], 
        check=True
    )
except subprocess.CalledProcessError as error:
    print(f"[{app_name}] Failed to set permissions: {error}")
    sys.exit(1)  # exit installer

# Verify app_name resolves within user's PATH

app_path = shutil.which(app_name)

if app_path:
    print(f"[{app_name}] {app_name} found at {app_path}")
    print(f"[{app_name}] Installation success!")
    exit(0)
else:
    print(f"[{app_name}] {app_name} not found: {app_path}")
    print(f"[{app_name}] Exiting installation:")
    exit(1)


