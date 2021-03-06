#!/usr/bin/python3

import sys
import subprocess
import os


def checkUsage():
    if(len(sys.argv) == 1):
        return 1
    elif(len(sys.argv) > 1):
        if(len(sys.argv) == 2):
            validatePath()
            return 1
        else:
            print("\nToo many arguments...❗\n")
            showUsageMessage()
            exit(1)
    else:
        exit(1)


def validatePath():
    print("\nValidating path...⌛\n")
    path = os.path.abspath(os.path.abspath(
        sys.argv[1]) + '/resources/app.asar')
    if(os.path.exists(path)):
        print("The path exists is correct...✅")
        return
    else:
        print("The path is not correct...❗")
        print("Please enter a valid path...❗")
        showUsageMessage()
        exit(1)


def showUsageMessage():
    print("Usage1: sudo ./crack.py \t⭐")
    print("Usage2: sudo ./crack.py '<Path_to_StarUML_Directory>' \t⭐")
    print("E.g: sudo ./crack.py '/opt/StarUML'")
    return


def checkSuperUserPrivilege():
    print("\nChecking Permissions...⌛\n")
    if(os.geteuid() != 0):
        print("You need to run the script as a superuser...👑❗\n")
        exit(1)
    else:
        return 1


def checkRequirements():
    print("Checking for requirements...⌛\n")
    output = subprocess.run(['node', '--version'],
                            capture_output=True, text=True)
    if(output.returncode):
        print("\n\"Node\" is not installed on this system...❗")
        print("Please install \"Node\" and run the script again...🔁")
        print("\n🔗*** https://nodejs.org/en/ ***🔗\n")
        exit(1)
    else:
        version = output.stdout.replace('\n', '')
        print(f"Node{version} installed...✅")
        output = subprocess.run(
            ['npm', 'list', '-g', 'asar'], capture_output=True, text=True)
        if(output.returncode):
            print("\n\"asar\" is not installed on this system❗")
            print("Please install \"asar\" and run the script again...🔁")
            print("\nRun \"npm install -g asar\" to install asar...⏬\n")
            exit(1)
        else:
            version = list(output.stdout.split(' '))[-1].replace('\n', '')
            print(f"{version} installed...✅")
            print("\nAll requirements fulfilled...💯\n")
            return 1


def extractAsarFile(asarFile, app):
    output = subprocess.run(
        ['asar', 'extract', asarFile, app], capture_output=True, text=True)
    if(output.returncode):
        print(output.stderr)
        print("\nHacking Failed...❌\n")
        exit(1)
    else:
        return 1


def packApp(app, outputAsar):
    output = subprocess.run(
        ['asar', 'pack', app, outputAsar], capture_output=True, text=True)
    if(output.returncode):
        print(output.stderr)
        print("\nHacking Failed...❌\n")
        exit(1)
    else:
        return 1


def cleanUp(asarBackup, asarFile, app, outputAsar):
    output = subprocess.run(['mv', asarFile, asarBackup],
                            capture_output=True, text=True)
    if(output.returncode):
        print(output.stderr)
        print("\nHacking Failed...❌\n")
        exit(1)
    else:
        output = subprocess.run(
            ['rm', '-rf', app, asarFile], capture_output=True, text=True)
        if(output.returncode):
            print(output.stderr)
            output = subprocess.run(
                ['mv', asarBackup, asarFile], capture_output=True, text=True)
            output = subprocess.run(
                ['rm', asarBackup], capture_output=True, text=True)
            print("\nError while cleaning...❕\n")
            print("\nHacking Failed...❌\n")
            exit(1)
        else:
            output = subprocess.run(
                ['mv', outputAsar, asarFile], capture_output=True, text=True)
            if(output.returncode):
                print(output.stderr)
                output = subprocess.run(
                    ['mv', asarBackup, asarFile], capture_output=True, text=True)
                output = subprocess.run(
                    ['rm', asarBackup], capture_output=True, text=True)
                print("\nError while cleaning...❕\n")
                print("\nHacking Failed...❌\n")
                exit(1)
            else:
                output = subprocess.run(
                    ['rm', asarBackup], capture_output=True, text=True)
                return 1


def modifyCode(app):
    print("Modifying code...⌛\n")
    license_manager = os.path.abspath(app + '/src/engine/license-manager.js')
    with open(license_manager, 'r') as f:
        data = f.read()
    data = data.replace('UnregisteredDialog.showDialog()',
                        '// UnregisteredDialog.showDialog()')
    with open(license_manager, 'w') as f:
        f.write(data)

    diagram_export = os.path.abspath(app + '/src/engine/diagram-export.js')
    with open(diagram_export, 'r') as f:
        data = f.read()
    data = data.replace('UNREGISTERED', '')
    with open(diagram_export, 'w') as f:
        f.write(data)

    about_dialog = os.path.abspath(app + '/src/dialogs/about-dialog.js')
    with open(about_dialog, 'r') as f:
        data = f.read()
    data = data.replace('UNREGISTERED', 'AFrostyPenguin')
    with open(about_dialog, 'w') as f:
        f.write(data)

    titlebar_view = os.path.abspath(app + '/src/views/titlebar-view.js')
    with open(titlebar_view, 'r') as f:
        data = f.read()
    data = data.replace('UNREGISTERED', 'Cracked by AFrostyPenguin')
    with open(titlebar_view, 'w') as f:
        f.write(data)


def crack():
    print("Starting the hack...💀\n")
    if(len(sys.argv) == 1):
        asarPath = os.path.abspath('/opt/StarUML/resources')
    else:
        asarPath = os.path.abspath(os.path.abspath(sys.argv[1]) + '/resources')
    asarFile = os.path.abspath(asarPath + '/app.asar')
    app = os.path.abspath(asarPath + '/app')
    if(extractAsarFile(asarFile, app)):
        modifyCode(app)
        outputAsar = os.path.abspath(asarPath + '/app2.asar')
        asarBackup = os.path.abspath(asarPath + '/app.asar.bak')
        if(packApp(app, outputAsar)):
            if(cleanUp(asarBackup, asarFile, app, outputAsar)):
                print("\nHacking Complete...💯✅\n")


if(checkUsage()):
    if(checkSuperUserPrivilege()):
        if(checkRequirements()):
            crack()
