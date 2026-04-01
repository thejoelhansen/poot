command = {
    "git search": {
        "name": "git search {pattern}",
        "body": f'git log -G"{{pattern}}" --oneline --patch',
        "help": (
            "Search git history for a line matching the given pattern.\n"
            "Usage: git search <pattern>\n"
            "Example: git search TODO"
        ),
        "runner": "shell"
    }
}
