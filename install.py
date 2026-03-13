#!/usr/bin/env python3


# --- Main !TODO 
## Make non sudo install path into user's home directory: Updating all paths to install $HOME/.poot/ if ran without sudo (IE python3 install.py)


# Library imports

import subprocess
import shutil
import glob
from pathlib import Path

# Check if Python version > 3.9
def check_python_version(min_version=(3, 9)):

    ## Get Python version string
    version_string = subprocess.run(
        ["python3", "--version"], 
        check=True, 
        capture_output=True, 
        text=True
    )

    ## Convert version string to number
    version_list = version_string.stdout.split()[1]
    version_tuple_string = tuple(version_list.split("."))
    version_number = tuple(map(int, version_tuple_string))
    
    ## Compare current installed version with minimum version 
    version_is_greater = version_number >= min_version
 
    return version_is_greater

# Guardrail: Fail if Python version is < 3.9
if __name__ == "__main__":
    version_check = check_python_version()
    
    if version_check == True:
        print("[poot] Success! Python minimum version is at least 3.9")
    else:
        print("[poot] Exiting installation: Python must be at least 3.9")
        exit(1)

# Create folders
def create_dirs(dir_list):
    for directory in dir_list:
        print(f"[poot] Creating {directory}")
        subprocess.run(["mkdir", "-p", directory], check=True)

create_dirs([
    "/usr/local/lib/poot/core",
    "/usr/local/lib/poot/modules"
])

# Copy files to default global install directory
def copy_file(source_file, destination_folder):
    for file in glob.glob(source_file): 
        print(f"[poot] Copying {file}")
        shutil.copy(file, destination_folder)

## Copy executable
copy_file("./poot", "/usr/local/bin/")
## Copy core files
copy_file("./core/*", "/usr/local/lib/poot/core/")
copy_file("./readme.MD", "/usr/local/lib/poot/")
copy_file("./install.py", "/usr/local/lib/poot/")
copy_file("./modules/*", "/usr/local/lib/poot/modules/")

# Verify install

## Collection missing files
missing = []

# !TODO Update with full install requirements

required_files = [
    "/usr/local/bin/poot",
    "/usr/local/lib/poot/core/dispatch.py",
    "/usr/local/lib/poot/core/run.py",
    "/usr/local/lib/poot/modules",
    "/usr/local/lib/poot/install.py"
]

## Check if required files exist, appending the missing files to missing[]
for path in required_files:
    if not Path(path).exists():
        missing.append(path)

## See if anything was added to missing[]
if missing:
    print("[poot] Failed to install:")
    for file in missing:
        print(f"- {file}")
        print("Exiting installation:")
        exit(1)

# Update executable permissions

try:
    subprocess.run(
        ["chmod", "755", "/usr/local/bin/poot"], 
        check=True
    )
except subprocess.CalledProcessError as error:
    print(f"[poot] Failed to set permissions: {error}")
    sys.exit(1)  # exit installer

# Verify poot resolves within user's PATH

poot_path = shutil.which("poot")

if poot_path:
    print(f"[poot] Poot found at {poot_path}")
    print("[poot] Installation success!")
    exit(0)
else:
    print(f"[poot] Poot not found: {poot_path}")
    print("[poot] Exiting installation:")
    exit(1)


