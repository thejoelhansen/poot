#!/usr/bin/env python3

# Import libraries

from pathlib import Path
import glob

# Dispatch to core/dispatch

def dispatch():
     
    # Locate /core directory
    # Precedence is pwd ./.poot/core > $HOME/.poot/core > /usr/local/lib/poot/core (later entries override earlier ones)
    core_directories = [
        Path("/usr/local/lib/poot/core"),
        Path.home().joinpath(".poot/core"),
        Path("./.poot/core")
    ]

    # Find all core libraries
    core_libraries = {}
    
    # List all fies in all core directories 
    for core_path in core_directories:
        if core_path.exists(): 
            # Update core library dict with files as they are found
            for library_path in core_path.glob('*.py'):
                core_libraries[library_path.stem] = str(core_path)
  
    # Required core files to ensure base app functionality
    required_core_files = [
        "run",
        "dispatch"
    ]

    def file_check(required_files, found_libraries):

        missing_files = []

        for file in required_files:
            if file not in found_libraries:
                missing_files.append(file)

        if missing_files:
            raise FileNotFoundError(f"[poot] Missing required core files: {missing_files}")
 
        return missing_files 

    output = file_check(required_core_files, core_libraries)
    print(output)
    exit()
!! HERE not working as expected. Fix file_check funciton, move to top, then finish module_libraries, and then run both libraries through the file check. THEN on to executing (importing) uh dispatch and probably run
    for path in core_paths:
        print(f"Checking {path} -> {path.exists()}") 
        if path.exists():
            core_dir = path 
            break
    else: 
        raise FileNotFoundError(f"[poot] No Core directory found: {path}")

    modules_paths = [
        Path("./.poot/modules"),
        Path.home().joinpath(".poot/modules"),
        Path("/usr/local/lib/modules")
    ]

    for path in modules_paths:
        if path.exists():
            modules_dir = path
            break
    else:
        raise FileNotFoundError(f"[poot] No Modules directory found: {path}")
                
    print(core_dir, modules_dir)


dispatch()
