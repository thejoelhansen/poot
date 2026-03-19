#!/usr/bin/env python3

# Import libraries

from pathlib import Path
import glob
import importlib.util
import sys
import configparser
#from runners.run_shell import run_shell

# App name
# Load config
config = configparser.ConfigParser()
config.read("config.ini")

# Get app name from config
app_name = config.get("APP", "app_name")

# Gather all core & custom runners & commands

def gather_modules():

    # Compare libraries found against a list of required library files
    def file_check(required_files, found_files):

        missing_files = []

        for file in required_files:
            if file not in found_files:
                missing_files.append(file)
        if missing_files:
            raise FileNotFoundError(f"[{app_name}] Missing required files: {missing_files}")

    # ----- Locate core runner directories
    
    # Precedence is pwd ./.app_name/runners > $HOME/.app_name/runners > /usr/local/lib/app_name/runners (later entries override earlier ones)
    core_runner_dir = [
        Path(f"/usr/local/lib/{app_name}/runners"),
        Path.home().joinpath(f".{app_name}/runners"),
        Path(f"./.{app_name}/runners")
    ]

    # Find all core runners 
    runners = {}
    
    # List files in core runners/ 
    for core_path in core_runner_dir:
        if core_path.exists(): 
            # Update core library dict with files as they are found
            for runner_path in core_path.glob('*.py'):
                runners[runner_path.stem] = str(core_path)

    # ----- Locate core modules directory
    
    # Precedence is pwd ./.app_name/modules > $HOME/.app_name/modules > /usr/local/lib/app_name/modules (later entries override earlier ones)
    core_command_dir = [
        Path(f"/usr/local/lib/{app_name}/commands"),
        Path.home().joinpath(f".{app_name}/commands"),
        Path(f"./.{app_name}/commands")
    ]

    # Find all core commands
    commands = {}
    
    # List files in core commands/
    for core_path in core_command_dir:
        if core_path.exists(): 
            # Update core module dict with files as they are found
            for command_path in core_path.glob('*.py'):
                commands[command_path.stem] = str(core_path)

    # Check found libraries and modules against required files

    # Required core modules to ensure base app functionality
    # TODO make into variable defined in config.ini for easy customization
    required_runners = [
        "run_shell"
    ]

    required_commands = [
    ]

    file_check(required_runners, runners)
    file_check(required_commands, commands)

    return runners, commands
    
# Run dispatch, catching missing file errors
try: 
    runners, commands = gather_modules()
    # DEBUG
    print(f"Found runners: {runners}, Found commands: {commands}")
except FileNotFoundError as error:
    print(error)
    exit(1)


cmd = "haai"
#run_shell(cmd)
