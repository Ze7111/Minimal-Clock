try:
    import requests, rich, tempfile, os
except Exception as e:
    import os
    string = str(e)
    module = string.split("'")[1].split("'")[0]
    os.system(f'pip install {module}')
    
from rich import console, progress
from src.r_config import Read; read = Read().get_default
from time import sleep

print = console.Console().print
progress = progress.Progress()

# Get the latest version of this program from GitHub
class Update:
    def getLatestVersion():
        # Get the latest release from GitHub
        latestRelease = requests.get('https://api.github.com/repos/ze7111/Minimal-Clock/releases/latest').json()
        # Get the latest version from the latest release
        latestVersion = latestRelease['tag_name']
        # Return the latest version
        return latestVersion
    
    def checkForUpdates():
        # Get the latest version
        latestVersion = Update.getLatestVersion()
        # Get the current version
        currentVersion = read('AppVersion')
        print(f"Current version: {currentVersion} | Latest version: {latestVersion}")
        # If the latest version is not the same as the current version
        if latestVersion != currentVersion:
            # Return True
            return True
        # If the latest version is the same as the current version
        else:
            # Return False
            return False
        
    def download_latest():
        # Get the latest release from GitHub
        latestRelease = requests.get('https://api.github.com/repos/ze7111/Minimal-Clock/releases/latest').json()
        # Get the latest version from the latest release
        latestVersion = latestRelease['tag_name']
        # Get the download link from the latest release
        downloadLink = latestRelease['assets'][0]['browser_download_url']
        
        temp_path = str(tempfile.gettempdir())
        
        try:
            os.mkdir(f'{temp_path}/Minimal-Clock/')
        except FileExistsError:
            pass
        
        
        # Download the latest release        
        with progress:
            task_id = progress.add_task("[red][bold]Downloading latest release...", start=False)
            progress.start_task(task_id)
            r = requests.get(downloadLink, allow_redirects=True)
            progress.update(task_id, total=int(r.headers.get('content-length', 0)))
            open(f'{temp_path}\\Minimal-Clock\\update {latestVersion}.zip', 'wb').write(r.content)
            progress.update(task_id, advance=len(r.content))
        # Return the latest version        
        return latestVersion
    
def main():
    

if Update.checkForUpdates() == True:
    print('Update available', style = 'bold red')
    Update.download_latest()
    print('Update downloaded', style = 'bold green')
    try:
        os.system('python3 .\\data\\overwrite.py')
    except:
        os.system('python .\\data\\overwrite.py')