import os, sys, shutil, tempfile, requests, zipfile

# delete evrthing in the root directory except for the data folder
def deleteAllFiles():
    for file in os.listdir():
        if file != 'data' and file != '.git':
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)

def copy_from_temp():
    # Get the latest release from GitHub
    latestRelease = requests.get('https://api.github.com/repos/ze7111/Minimal-Clock/releases/latest').json()
    # Get the latest version from the latest release
    latestVersion = latestRelease['tag_name']
    # Get the download link from the latest release
    temp_path = str(tempfile.gettempdir())
    
    copy_from_path = f'{temp_path}\\Minimal-Clock\\update {latestVersion}.zip'
    
    current_path = os.getcwd().split('\\')[-1]
    
    with zipfile.ZipFile(copy_from_path, 'r') as zip_ref:
        zip_ref.extractall(current_path.split('\\')[-1])
    

    # move files from the Minimal-Clock folder to the root directory
    for file in os.listdir('./Minimal-Clock/'):
        shutil.move(f'./Minimal-Clock/{file}', '.\\')
        
    os.rmdir('./Minimal-Clock/')

def run():
    try:
        os.system('python3 .\\app.py')
    except:
        os.system('python .\\app.py')

deleteAllFiles()
copy_from_temp()
run()
