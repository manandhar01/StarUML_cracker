#!/usr/bin/python3

import subprocess
import os


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
        print("\"Node\" is not installed on this system...❗")
        print("Please install \"Node\" and run the script again...🔁")
        exit(1)
    else:
        version = output.stdout.replace('\n', '')
        print(f"Node{version} installed...✅")
        output = subprocess.run(
            ['npm', 'list', '-g', 'asar'], capture_output=True, text=True)
        if(output.returncode):
            print("\"asar\" is not installed on this system❗")
            print("Please install \"asar\" and run the script again...🔁")
            print("Your can install it with \"npm install -g asar\"⏬")
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


def cleanUp(asarPath, asarFile, app, outputAsar):
    asarBackup = asarPath + 'app.asar.bak'
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
            exit(0)
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
            else:
                output = subprocess.run(
                    ['rm', asarBackup], capture_output=True, text=True)
                return 1


def modifyCode(app):
    print("Modifying code...⌛\n")
    license_manager = app + '/src/engine/license-manager.js'
    with open(license_manager, 'r') as f:
        data = f.read()
    data = data.replace('UnregisteredDialog.showDialog()',
                        '// UnregisteredDialog.showDialog()')
    with open(license_manager, 'w') as f:
        f.write(data)

    diagram_export = app + '/src/engine/diagram-export.js'
    with open(diagram_export, 'r') as f:
        data = f.read()
    data = data.replace('UNREGISTERED', '')
    with open(diagram_export, 'w') as f:
        f.write(data)

    about_dialog = app + '/src/dialogs/about-dialog.js'
    with open(about_dialog, 'r') as f:
        data = f.read()
    data = data.replace('UNREGISTERED', 'AFrostyPenguin')
    with open(about_dialog, 'w') as f:
        f.write(data)

    titlebar_view = app + '/src/views/titlebar-view.js'
    with open(titlebar_view, 'r') as f:
        data = f.read()
    data = data.replace('UNREGISTERED', 'Cracked by AFrostyPenguin')
    with open(titlebar_view, 'w') as f:
        f.write(data)


def crack():
    print("Starting the hack...💀\n")
    asarPath = '/opt/StarUML/resources/'
    asarFile = asarPath + 'app.asar'
    app = asarPath + 'app'
    if(extractAsarFile(asarFile, app)):
        modifyCode(app)
        outputAsar = asarPath + 'app2.asar'
        if(packApp(app, outputAsar)):
            if(cleanUp(asarPath, asarFile, app, outputAsar)):
                print("\nHacking Complete...💯✅\n")


if(checkSuperUserPrivilege()):
    if(checkRequirements()):
        crack()
