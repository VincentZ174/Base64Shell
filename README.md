# Base64Shell
A multiclient python reverse shell that encodes commands being sent to the victim machine and output sent to the attacker machine in base64.

# Important
- Don't forget to change the HOST field in the shell file to the victim's 
- Make sure you run the server first
- Written in python 2.7

# Usage 
Server: python server.py  
Victim: python shell.py(converting the shell.py file to an exe and sending it to the victim is a better idea)

# Features
- Ctrl-C to refresh list of connected victims
- Download -  Type in "download filename" to download a file from the victim machine 
- Upload - Type in "upload filename" to upload a file from the attack machine
- Example: download 1.txt , upload 1.txt
- Quit - type "quit" to exit

# Extra  
Convert shell.py to exe using Py2exe(http://www.py2exe.org)

