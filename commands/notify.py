# Notes: 

# --- Name !Required
# Command "name" is called after {app_name} to execute the command "body". It is case-sensitive. 

# --- Body !Required 
# Define body of command, placing "{variable_name}" in double quotes

# --- Help Text !Required
# Help text for main app --help as well as missing/ misspelled argument or subcommand

# --- Runner ! Required
# Specify the runner through which the command should be executed through - usually coincides with a language (bash shell or python) or a specific version (python2 or python3)

# --- Usage
# Second line of help text to provide a usage example of the command. Wrap in {'Usage:':<18} to get a nice, right-align

# --- Arguments 
# Define variables as {variable_name} for use in "body"

commands = {
    "docker test": {
        "arguments": "{arg1}",
        "body": 'docker run --rm busybox echo "{arg1}"',
        "help": "Docker hello world test.",
        "usage": (
            f"{'Usage:':<18} docker command <pattern>\n"
            f"{'Example:':<18} docker command containername"
        ),
        "runner": "shell"
    },
    "docker test2": {
        "arguments": "{arg2}",
        "body": 'docker run --rm busybox echo "{arg2}"',
        "help": "Another docker command.",
        "usage": (
            f"{'Usage:':<18} docker command <pattern>\n"
            f"{'Example:':<18} docker command containername"
        ), 
        "runner": "shell"
    }
}
