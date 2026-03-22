## -- Testing - from app_root/commands/ping.py
# import sys
# import subprocess
# import shutil
# import glob
# from pathlib import Path
# import configparser
#
# command = {
#     "name":"ping-server",
#     "body":"ping -c 1 1.1.1.1",
#     "help":"Help text for help with using this command",
#     "runner":"shell"
# }
#
# ping_command = command # becomes ping.command in pot.py, but should be abstracted to <user_supplied_command>.command
# # {'name': 'ping-server', 'body': 'ping 0.0.0.0', 'help': 'Help text for help with using this command', 'runner': 'shell'}
#
## -- end of testing 

def run(cmd):
    # 1 initial test - delete later
    #print(f"Running: {cmd}")
    #return f"Executed {cmd}"

    split_command = cmd["body"].split() # () instead of (" ") in case typos with double space, or returns
    
    try:
        output = subprocess.run(
            split_command,
            check=True,
            capture_output=True,
            text=True
        )
        print(output.stdout)

    except subprocess.CalledProcessError as error:
        print("Command failed")
        print("Return code:", error.returncode)
        print("Error output:", error.stderr)

    # If app <command> --help is present then display help text & exit

    # Take cmd[body] and split it and then shove it into run.subprocess for clean execution

# run(ping_command)
