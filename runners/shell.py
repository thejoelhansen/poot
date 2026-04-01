## -- Testing - from app_root/commands/ping.py

import subprocess
import shlex

def run(parsed_command):

    cmd = parsed_command["parsed_body"]

    print(f"Running: {cmd}")  # debug

    try:
        output = subprocess.run(
            shlex.split(cmd), # Safer than split(), according to stack overflow 
            check=True,
            capture_output=True,
            text=True
        )
        print(output.stdout)

    except subprocess.CalledProcessError as error:
        print("Command failed")
        print("Return code:", error.returncode)
        print("Error output:", error.stderr)
