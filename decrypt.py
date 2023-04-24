from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import os
import base64
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


def decrypt(dataFile, privateKeyFile):
    
    #use EAX mode to allow detection of unauthorized modifications
    
    path_to_save = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt'
    fileToRead = os.path.join(path_to_save,dataFile)
    # read private key from file
    with open(privateKeyFile, 'rb') as f:
        privateKey = f.read()
        # create private key object
        key = RSA.import_key(privateKey)

    # read data from file
    with open(fileToRead, 'rb') as f:
        # read the session key
        encryptedSessionKey, nonce, tag, ciphertext = [ f.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

    # decrypt the session key
    cipher = PKCS1_OAEP.new(key)
    sessionKey = cipher.decrypt(encryptedSessionKey)

    # decrypt the data with the session key
    cipher = AES.new(sessionKey, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # save the decrypted data to file
    #[ fileName, originalFileExtension, fileExtension ] = dataFile.split('.')
    fileDetails = dataFile.split('.')
    fileName = fileDetails[0]
    originalFileExtension = fileDetails[1]
    fileExtenstion = ''
    fileToRemove = ''
    
    
    if(len(fileDetails) == 2):
    	fileExtension = originalFileExtension
    	fileToRemove = fileName + '.' + fileExtension
    else:
    	fileExtension = fileDetails[2]
    	fileToRemove = fileName + '.' + originalFileExtension + '.' + fileExtension
    
    
    decryptedFile = fileName + '.' + originalFileExtension
   
    #print(decryptedFile)
    
    completePath = os.path.join(path_to_save,decryptedFile)
    
    with open(completePath, 'wb') as f:
        f.write(data)

    print('Decrypted file saved to ' + decryptedFile)
    #fileToRemove = fileName + '.' + originalFileExtension + '.' + fileExtension
    pathName = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt/' + fileToRemove
    if fileExtension != 'txt':
    	os.remove(pathName)
    

'''
def decrypt(dataFile, privateKeyFile):
    
    #use EAX mode to allow detection of unauthorized modifications
    
	
    path_to_save = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt'
    fileToRead = os.path.join(path_to_save,dataFile)
	
    # read private key from file
    with open(privateKeyFile, 'rb') as f:
        privateKey = f.read()
        # create private key object
        key = RSA.import_key(privateKey)

    # read data from file
    with open(fileToRead, 'rb') as f:
        # read the session key
        encryptedSessionKey, nonce, tag, ciphertext = [ f.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

    # decrypt the session key
    cipher = PKCS1_OAEP.new(key)
    sessionKey = cipher.decrypt(encryptedSessionKey)

    # decrypt the data with the session key
    cipher = AES.new(sessionKey, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # save the decrypted data to file
    #[ fileName, fileExtension ] = dataFile.split('.')
    
    fileDetails = dataFile.split('.')
    fileName = fileDetails[0]
    originalFileExtension = fileDetails[1]
    fileExtenstion = ''
    fileToRemove = ''
    if(len(fileDetails) == 2):
    	fileExtension = originalFileExtension
    	fileToRemove = fileName + '.' + originalFileExtension + '.' + fileExtension
    else:
    	fileExtension = fileDetails[2]
    	fileToRemove = fileName + '.' + originalFileExtension + '.' + fileExtension
    
    decryptedFile = fileName + '.' + originalFileExtension
    with open(decryptedFile, 'wb') as f:
        f.write(data)

    print('Decrypted file saved to ' + decryptedFile)
    
    pathName = '/home/vaisakh/Desktop/pythawn/test.vexps'
  #  os.remove(pathName)
    
'''
#decrypt("exp5.pdf","private.pem")

def decryptAllFiles(): 
 
	directory = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt' # CHANGE THIS
	excludeExtension = ['.py','.pem', '.exe'] # CHANGE THIS
	for item in scanRecurse(directory): 
            filePath = Path(item)
            filePath = str(filePath)
            filePath = filePath.split('/')
            #print(filePath[-1])
            requiredFile = filePath[-1].split('.')
            #print(requiredFile)
            requiredFileName = requiredFile[0]
            fileType = requiredFile[len(requiredFile) - 1]
            '''
            if len(requiredFile) == 3:
            	fileType = requiredFile[2]
            else:
            	fileType = requiredFile[1]
	    '''
            if fileType in excludeExtension:
                continue
           # print(filePath[-1])
            decrypt(filePath[-1], "private.pem")
            

decryptAllFiles()
