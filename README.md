# pot
Programmable Operations Tool

# General Use

# TODO
- add dryrun flag
- add argument type
- move required runners, commands, files into config

# Modules

# Core Modules

Default "core" modules are provided in the install package under ./modules. These are installed by default to /usr/local/lib/pot/modules and available if poot was installed globally. 

If pot should be installed local to the user, IE ~/.pot, then these core modules are installed by default to ~/.pot/modules. 

# Installation

To install globally run: 

```
sudo python3 install.py
```

To install locally for the current user: 
```
python3 install.py
```

Note: The installer will ask. 
Note: The dedault app name is 'pot'. If you'd like to change this you'll need to update two things:
- config.ini > app_name = "new-app-name"
- mv pot.py new-app-name

# Updating
