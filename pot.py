#!/usr/bin/env python3

# --- Basic Structure
# 1 Import standard libraries & local config
# 2 Scan install directories for runner & command modules
# 3 Import modules as libraries and alias them
# 4 Parse user input command and execute through specified runner
# 5 !! TODO Hook command output to 'Output' module for notification (slack, teams, discord)

# Import libraries

from pathlib import Path
import glob
import importlib.util
import sys
import configparser
import re

# App name
# Load config
config = configparser.ConfigParser()
config.read("config.ini")

# Get app name from config
app_name = config.get("APP", "app_name")

# Load all corem, custom runners & commands

def load_modules():

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
                # Skip __init__ module file
                if runner_path.stem == "__init__":
                    continue
                
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

                # Build module.command for each module found in /commands/*
                module_name = f"commands.{command_path.stem}"
                spec = importlib.util.spec_from_file_location(module_name, command_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Skip files without `commands`
                if not hasattr(module, "commands"):
                    continue

                # Required command keys (fields) 
                required_keys = {"body", "runner", "help"}
               
                # Merge commands from file
                for command_name, command_def in module.commands.items():
                    if not required_keys.issubset(command_def):
                        print(f"Skipping invalid command: {command_name} in {command_path}")
                        continue
                  
                    # Set non-essential keys if missing
                    if "arguments" not in command_def:
                        command_def["arguments"] = ""
                    if "usage" not in command_def:
                        command_def["usage"] = ""

                    # Assign command definition and source location (for use in --help) 
                    commands[command_name] = {
                        **command_def,
                        "_source": str(command_path)
                    }

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
    runners, commands = load_modules()
    # print(f"DEBUG Found runners: {runners}, Found commands: {commands}") # DEBUG
except FileNotFoundError as error:
    print(error)
    exit(1)

# Assemble {app_name} Help Text

# General header
help_header = f"""
{app_name}: CLI Command Wrapper

Usage:
  {app_name} <command> [args]

Options:
  -h, --help        Show this help message

Commands:
"""

help_commands = ""

# Assemble available Commands from imported_commands
for name, cmd in commands.items():
    desc = cmd.get("help", "")
    usage = cmd.get("usage", "")
    source = cmd.get("_source", "")

    help_commands += f"  {name:<18}{desc}\n"
    
    if usage:
        for line in usage.split("\n"):
            help_commands += f"  {'':<18}{line}\n"

    help_commands += f"  {'':<18}({source})\n"

# Combine header & imported_commands
help_text = help_header + help_commands

# TODO Parser... add support for typed arguments {arg1:int} or {arg2:str} for faster failing & safer input handling (arg = ; rm -rf ... yikes)

def parse_input(user_arg, commands):

    # Define app & command help flags
    help_flags = ["help", "-help", "--help", "-h"]

    # Return app help text 
    if not user_arg or user_arg[0] in help_flags:
        print(help_text)
        exit(0)

    input_str = " ".join(user_arg)

    arg_names = []

    # Split user's commands into individual tokens (candidate) within a list
    for i in range(len(user_arg), 0, -1):
        candidate = " ".join(user_arg[:i])
        
        print("DEBUG: Checking candidate:", repr(candidate)) # DEBUG

        # Try first exact match
        if candidate in commands:
            cmd = commands[candidate]
            args = user_arg[i:]

            # Return command help text
            if any(flag in args for flag in help_flags):
                print(cmd.get("help", "No help available."))
                exit(0)

            print("DEBUG: Matched command:", candidate) # DEBUG

            # Extract arg names from "name"
            arg_names = re.findall(r"{(\w+)}", cmd.get("arguments", ""))

            # 🔥 Map args → arg names
            arg_map = {}
            for idx, arg_name in enumerate(arg_names):
                if idx < len(args):
                    arg_map[arg_name] = args[idx]
                else:
                    print(f"Missing argument: {arg_name}")
                    exit(1)

            # 🔥 Format body
            try:
                formatted_body = cmd["body"].format(**arg_map)
            except KeyError as e:
                print(f"Argument mismatch: {e}")
                exit(1)

            cmd["parsed_body"] = formatted_body

            return cmd, args

    # Catch partially missing commands
    base_input = " ".join([arg for arg in user_arg if arg not in help_flags])

    partial_matches = [
        name for name in commands
        if name.startswith(base_input)
    ]

    # Print command help text
    if partial_matches:
        print("Available subcommands:\n")
        for name in partial_matches:
            desc = commands[name].get("help", "")
            print(f"  {name:<18}{desc}")
        exit(0)

    return None, []

# Get user's commands after app (pot)
user_arg = sys.argv[1:]

try: 
    parsed_command, parsed_arg = parse_input(user_arg, commands)
    
    if parsed_command is None:
        print(f"Unknown command: {' '.join(user_arg)}\n")
        print("Available commands:\n")
        for name in commands:
            print(f"    {name:<18}{desc}")
        exit(1)

    # DEBUG
    # print(parsed_command, parsed_arg); exit()
except FileNotFoundError as error:
    print(error)
    exit(1)

# Load runner module 
runner_name = parsed_command["runner"]

if runner_name not in runners:
    print(f"Runner '{runner_name}' not found")
    exit(1)

runner_path = Path(runners[runner_name]) / f"{runner_name}.py"

spec = importlib.util.spec_from_file_location(f"runners.{runner_name}", runner_path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

# Run command
runner.run(parsed_command)
