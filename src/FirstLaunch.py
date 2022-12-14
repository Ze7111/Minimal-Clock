import os

blob = r"""import os, shutil, tempfile, requests, zipfile

def deleteAllFiles(): # delete all files in the root directory
    for file in os.listdir(): # iterate over all the files in the directory
        if file != 'data' and file != '.git': # check whether the file is a data folder or a .git folder
            if os.path.isfile(file): # check whether the file is a file or a directory
                os.remove(file) # delete the file
            elif os.path.isdir(file): # check whether the file is a directory
                shutil.rmtree(file) # delete the directory
 
def copy_from_temp(): # copy the files from the temp directory to the root directory
    # Get the latest release from GitHub
    latestRelease = requests.get('https://api.github.com/repos/ze7111/Minimal-Clock/releases/latest').json()
    # Get the latest version from the latest release
    latestVersion = latestRelease['tag_name']
    # Get the download link from the latest release
    temp_path = str(tempfile.gettempdir())
    # Download the latest release
    copy_from_path = f'{temp_path}\\Minimal-Clock\\update {latestVersion}.zip'
    # Copy the files from the downloaded release
    current_path = os.getcwd().split('\\')[-1]
    # Copy the files from the downloaded release
    with zipfile.ZipFile(copy_from_path, 'r') as zip_ref:
        zip_ref.extractall(current_path.split('\\')[-1])
    # Delete the downloaded release
    for file in os.listdir('./Minimal-Clock/'):
        shutil.move(f'./Minimal-Clock/{file}', '.\\')
    # move files from the Minimal-Clock folder to the root directory
    os.rmdir('./Minimal-Clock/')
    # Delete the Minimal-Clock folder
    
def run(): # run the script
    try: # try to run the script
        os.system('python3 .\\app.py') # run the app in python3
    except: # if the script fails to run in python3
        os.system('python .\\app.py') # run the app in python

if __name__ == '__main__': # run the script if it is the main script
    deleteAllFiles() # delete all files in the root directory
    copy_from_temp() # copy the files from the temp directory to the root directory
    run() # run the script
else: # if the script is not the main script
    print('Process failed to run with error [0x053DLL]') # print a message"""
    
class setup:
    def write_to_file(self) -> None:
        line_no = 0
        try:
            os.mkdir('data')
        except FileExistsError:
            pass
        
        with open('data/overwrite.dll', 'w') as f:
            f.write(blob)
            f.close
            
        with open('config.ini', 'r') as f:
            data = f.readlines()
            f.close()
        
        for i in data:
            if i.startswith('FirstLaunch'):
                data[line_no] = 'FirstLaunch = False'
            line_no += 1
        
        with open('config.ini', 'w') as f:
            f.writelines(data)
            f.close()

        
setup().write_to_file()
