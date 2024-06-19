import os
from win32com.client import Dispatch

def check_for_start_shell(shortcut_name):
        print("Checking start up config")
        # Get the path to the user's startup folder
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        startup_files = os.listdir(startup_folder)# List all files in the startup folder
        if shortcut_name in startup_files:
            return True
        return False

def add_start_shell(program_path,shortcut_name):
    print("Adding to start up")
    startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    # This line constructs the full path to the shortcut file in the startup folder
    shortcut_path = os.path.join(startup_folder, shortcut_name)

    shell = Dispatch('WScript.Shell') # Create the shortcut
    shortcut = shell.CreateShortCut(shortcut_path)  # This line creates a shortcut object at the specified path

    # These lines set the target path and working directory of the shortcut
    shortcut.Targetpath = program_path
    shortcut.WorkingDirectory = os.path.dirname(program_path)

    shortcut.save()# This line saves the shortcut to the startup folder
    return shortcut
