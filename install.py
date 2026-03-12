#!/usr/bin/env python3

# Library imports

import subprocess
import shutil
import glob

# Check if Python is installed > versions 3.9
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
        print("[poot] Python minimum version is at least 3.9 - success!")
    else:
        print("[poot] Python must be at least 3.9 - exiting...")
        exit(1)

# Create folders
def create_dirs(dir_list):
    for directory in dir_list:
        subprocess.run(["mkdir", "-p", directory], check=True)

create_dirs(
    "/usr/local/bin/poot/core",
    "/usr/local/lib/poot/modules"
)

# Copy files to default global install directory
def copy_file(source_file, destination_folder):
    for file in glob.glob(source_file): 
        shutil.copy(file, destination_folder)

copy_file("./core/*", "/usr/local/bin/poot/core/")
copy_file("./readme.MD", "/usr/local/bin/poot/")
copy_file("./install.py", "/usr/local/bin/poot/")
copy_file("./poot", "usr/local/bin/poot/")
copy_file("./modules/*", "/usr/local/lib/poot/modules/")



# Try/catch to create /usr/local/lib/poot/modules

# Try to resolve the poot app via local PATH to ensure existing path just owrks for users
