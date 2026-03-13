#!/usr/bin/env python3

# Import libraries

from pathlib import Path

# Dispatch to core/dispatch

def dispatch():
    
    # Locate /core directory
    core_paths = [
        Path("./.poot/core"),
        Path.home / ".poot/core"),
        Path("/usr/local/lib/core")
    ]

    for core_install in core_paths:
        if core_install.exists():
            core_dir = core_install
            break
        else: 
            print(f"[poot] {core_install} not found.")
            raise FileNotFoundError(f"[poot] Core directory not found: {core_install}")

    module_paths = [
        Path("./.poot/modules"
                

dispatch()
