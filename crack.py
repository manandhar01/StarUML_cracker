#!/usr/bin/python3

import subprocess

print()
print("Checking for requirements...")
output = subprocess.run(
    'node --version', capture_output=True, text=True, shell=True)
if(output.returncode):
    print("\"Node\" is not installed on this system.")
    print("Please install \"Node\" and run the script again.")
else:
    output = subprocess.run(
        'npm list -g asar', capture_output=True, text=True, shell=True)
    if(output.returncode):
        print("\"asar\" is not installed on this system.")
        print("Please install \"asar\" and run the script again.")
        print("Your can install it with npm install -g asar")
    else:
        print()
        print("All Good...")
        print("Starting the hack...")
