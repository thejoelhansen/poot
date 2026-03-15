#!/usr/bin/env python3

# Import libraries

from pathlib import Path
import glob

# Dispatch to core/dispatch

def dispatch():

    # Compare libraries found against a list of required library files
    def file_check(required_files, found_files):

        missing_files = []

        for file in required_files:
            if file not in found_files:
                missing_files.append(file)
        if missing_files:
            raise FileNotFoundError(f"[poot] Missing required files: {missing_files}")

    # ----- Locate core libraries directory
    
    # Precedence is pwd ./.poot/core > $HOME/.poot/core > /usr/local/lib/poot/core (later entries override earlier ones)
    core_directories = [
        Path("/usr/local/lib/poot/core"),
        Path.home().joinpath(".poot/core"),
        Path("./.poot/core")
    ]

    # Find all core libraries
    libraries = {}
    
    # List all fies in all core directories 
    for core_path in core_directories:
        if core_path.exists(): 
            # Update core library dict with files as they are found
            for library_path in core_path.glob('*.py'):
                libraries[library_path.stem] = str(core_path)

    # ----- Locate core modules directory
    
    # Precedence is pwd ./.poot/modules > $HOME/.poot/modules > /usr/local/lib/poot/modules (later entries override earlier ones)
    modules_directories = [
        Path("/usr/local/lib/poot/modules"),
        Path.home().joinpath(".poot/modules"),
        Path("./.poot/modules")
    ]

    # Find all core modules
    modules = {}
    
    # List all fies in all core directories 
    for modules_path in modules_directories:
        if modules_path.exists(): 
            # Update core module dict with files as they are found
            for module_file in modules_path.glob('*.py'):
                modules[module_file.stem] = str(modules_path)

    # Check found libraries and modules against required files

    # Required core files to ensure base app functionality
    required_libraries = [
        "run",
        "dispatch"
    ]

    # !! TODO  Required modules. I haven't decided if there will be any yet.
    required_modules = [
    ]

    file_check(required_libraries, libraries)
    file_check(required_modules, modules)

    return libraries, modules
    
# Run dispatch, catching missing file errors
try: 
    libraries, modules = dispatch()
    # DEBUG
    # print(f"Found libraries: {libraries}, Found modules: {modules}")
except FileNotFoundError as error:
    print(error)
    exit(1)

