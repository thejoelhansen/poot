#!/usr/bin/env python3

# Import libraries

from pathlib import Path
import glob
import importlib.util
import sys
import configparser

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
        "shell"
    ]

    required_commands = [
    ]

    file_check(required_runners, runners)
    file_check(required_commands, commands)

    return runners, commands
    
# Gather modules
try: 
    runners, commands = gather_modules()
    # DEBUG
    ## print(f"Found runners: {runners}, Found commands: {commands}")
except FileNotFoundError as error:
    print(error)
    exit(1)

# Import found modules
def import_modules(modules, namespace):
    # Empty dict to track loaded modules
    loaded = {}
    
    for module, path in modules.items():
        if module == "__init__":
            continue
      
        # Construct module path 
        module_path = Path(path) / f"{module}.py"
        module_name = f"{namespace}.{module}"

        # Skip import if module already loaded
        if module in sys.modules:
            loaded[module] = sys.modules[module_name]
            continue

        # Create blueprint for module from runner name & modified module_path
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        import_module = importlib.util.module_from_spec(spec)
       
        # Import module
        sys.modules[module_name] = import_module
        spec.loader.exec_module(import_module)

        # Add imported module to loaded{}
        loaded[module] = import_module

    return loaded

# Import modules
imported_runners = import_modules(runners, "runners")
imported_commands = import_modules(commands, "commands")
# DEBUG
## print(imported_runners, imported_commands)

# Alias all runners and commands
## Runner functions are now shell.run() and Command dicts are now ping.cmd[]
for imported_modules in (imported_runners, imported_commands):
    for name, module in imported_modules.items():
        globals()[name] = module

# TODO 1 - NOT HERE - Go flesh out run_shell.py runner, taking (cmd), expanding it, and pumping it through run.subprocess

# TODO 2 Parse user input

# def parse_command():

# TODO 3 Run provided command through specified runner
 
# def run_command():


# !! TODO currently hardcoded

cmd = "haai"
shell.run(cmd)
print(ping.command)
