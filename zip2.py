import os
import pyminizip
from pathlib import Path

def scanRecurse(baseDir):
    '''
    Scan a directory and return a list of all files
    return: list of files
    '''
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)

folder_path = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt'
parent_folder = os.path.dirname(folder_path)

def progress_handler(fileName, percent):
	
	print(f"{fileName} : {percent}%")

def passwordLockTheFolder():
    listOfFiles = []
    directory = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt' # CHANGE THIS
    excludeExtension = ['.py','.pem', '.exe'] # CHANGE THIS
    for item in scanRecurse(directory): 
            filePath = Path(item)
            filePath = str(filePath)
            filePath = filePath.split('/')
            #print(filePath[-1])
            requiredFile = filePath[-1].split('.')
            requiredFileName = requiredFile[0]
            fileType = requiredFile[1]

            if fileType in excludeExtension:
                continue
            else:
                fileToCompress = os.path.join(directory,filePath[-1])
                listOfFiles.append(fileToCompress)
        
    #print(f"listOfFiles: {listOfFiles}")
    #print(f"progress_handler: {progress_handler}")
    pyminizip.compress_multiple(listOfFiles,[],"lockedFiles.zip", "1234", 2, progress_handler)
