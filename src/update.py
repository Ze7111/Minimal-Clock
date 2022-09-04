try: # try to import the required modules
    import requests, rich, tempfile, os, subprocess # requests for downloading the file, rich for the progress bar, tempfile for the temporary file, and os for the file operations
except Exception as e: # if there is an error
    import subprocess, sys # type: ignore
    string = str(e) # convert the error to a string
    module = string.split("'")[1].split("'")[0] # get the module name
    try: # try to install the module
        subprocess.run([sys.executable, "-m", "pip", "install", module]) # install the module
    except Exception as e: # if the user doesn't have pip installed
        print(f'Error: {e}') # print the error
    print("Please restart the program.") # tell the user to restart the program
    sys.exit(0) # exit the program
    
from rich import console, progress # import the console and progress bar from rich
from src.r_config import Read # import the module for reading the config file
from subprocess import Popen as pop # import the Popen function from subprocess
read = Read().get_default # import the config reader and get the default config
done = False # set the done variable to False
print = console.Console().print # set the print function to the rich console print function
progress = progress.Progress() # create the console and progress bar

# Get the latest version of this program from GitHub
class Update: # create the class
    def getLatestVersion(): # get the latest version
        # Get the latest release from GitHub
        latestRelease = requests.get('https://api.github.com/repos/ze7111/Minimal-Clock/releases/latest').json()
        # Get the latest version from the latest release
        latestVersion = latestRelease['tag_name']
        # Return the latest version
        return latestVersion
    
    def checkForUpdates(): # check for updates
        global done
        # Get the latest version
        latestVersion = Update.getLatestVersion() # get the latest version
        # Get the current version
        currentVersion = read('AppVersion') # get the current version
        if done == False: # if the update has not been done
            if latestVersion != currentVersion:
                print(f"[red][bold]Current version: [red]{currentVersion} [white][bold]| [green][bold]Latest version: [red]{latestVersion}") # print the current and latest version
            elif latestVersion == currentVersion:
                print(f"[green][bold]Current version: [red]{currentVersion} [white][bold]| [green][bold]Latest version: [red]{latestVersion}")
            done = True # set the done variable to True
        # If the latest version is not the same as the current version
        if latestVersion != currentVersion: # if the latest version is not the same as the current version
            # Return True
            return True # return true
        else: # if the latest version is the same as the current version
            # Return False
            return False # return false
        
    def download_latest(): # download the latest version
        # Get the latest release from GitHub
        latestRelease = requests.get('https://api.github.com/repos/ze7111/Minimal-Clock/releases/latest').json()
        # Get the latest version from the latest release
        latestVersion = latestRelease['tag_name']
        # Get the download link from the latest release
        downloadLink = latestRelease['assets'][0]['browser_download_url']
        # get the temporary directory
        temp_path = str(tempfile.gettempdir()) 
        # get the file name
        try: # try to get the file name
            os.mkdir(f'{temp_path}/Minimal-Clock/') # create the directory
        except FileExistsError: # if the directory already exists
            pass # do nothing
        # Download the latest release        
        with progress: # start the progress bar
            task_id = progress.add_task("[red][bold]Downloading latest release...", start=False) # add the task to the progress bar
            progress.start_task(task_id) # start the task
            r = requests.get(downloadLink, allow_redirects=True) # get the file
            progress.update(task_id, total=int(r.headers.get('content-length', 0))) # update the progress bar
            open(f'{temp_path}\\Minimal-Clock\\update {latestVersion}.zip', 'wb').write(r.content) # write the file to the temporary directory
            progress.update(task_id, advance=len(r.content)) # update the progress bar    
        return latestVersion # return the latest version

def main():
    if Update.checkForUpdates() == True: # if there is an update
        print('Update available', style = 'bold red') # print that there is an update
        Update.download_latest() # download the latest version
        print('Update downloaded', style = 'bold green') # print that the update has been downloaded
        try: # try to run the overwrite script in python3
            pop('python3 .\\data\\overwrite.dll', shell=True) # run the overwrite script
        except Exception: # if the user doesn't have python3 installed
            pop('python .\\data\\overwrite.dll', shell=True) # run the overwrite script in python
    if Update.checkForUpdates() == False: # if there is no update
        print('You are already up to date', style = 'bold green') # print that the user is up to date
