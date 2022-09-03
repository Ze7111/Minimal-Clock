import os, sys, shutil

# delete evrthing in the root directory except for the data folder
def deleteAllFiles():
    for file in os.listdir():
        if file != 'data':
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                shutil.rmtree(file)