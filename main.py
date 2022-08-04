import os
from tkinter import filedialog
from sys import platform
import rsa
from colorama import init
init()
from colorama import Fore




files_list = []


def open_folder():
    """Open a file dialog and ask to choose a folder

    Returns:
        string: path to the folder
    """
    
    f = filedialog.askdirectory(initialdir="C:/", title="Select a folder")
    return f

def add_files_to_list(folder):
    """Add all file and folder names in the given folder to the list

    Args:
        folder (string): the path to the folder
    """
    if platform == "win32":
        current_py_file = __file__.split("\\")[-1]
    else:
        current_py_file = __file__.split("/")[-1]
            
    blacklisted_files = [".pem", current_py_file]
    
    # List all files in the folder and subfolders
    for path, subdirs, files in os.walk(folder):
        for name in files:
            if not any(ext in name for ext in blacklisted_files):
                files_list.append(os.path.join(path, name))
            


def encrypt(message_to_encrypt, key):
    """Encrypt a message with the given key

    Args:
        message_to_encrypt (string): The message to encrypt
        key (string): The key to use for encryption

    Returns:
        string: the encrypted message
    """
    return rsa.encrypt(message_to_encrypt, key)



def decrypt(message_to_decrypt, key):
    """Decrypt a message with the given key

    Args:
        message_to_decrypt (string): The message to decrypt
        key (string): The key to use for decryption

    Returns:
        mixed: The decrypted message or a False if it couldn't be decrypted
    """
    try:
        return rsa.decrypt(message_to_decrypt, key)
    except:
        return False



def generate_keys():
    """Generate a public and private key and save them to the keys folder
    if they don't exist already
    """
    if not os.path.exists("keys/publicKey.pem") and not os.path.exists("keys/privateKey.pem"):
        os.makedirs("keys")
        
        (publicKey, privateKey) = rsa.newkeys(1024)
        with open('keys/publicKey.pem', 'wb') as p:
            p.write(publicKey.save_pkcs1('PEM'))
        with open('keys/privateKey.pem', 'wb') as p:
            p.write(privateKey.save_pkcs1('PEM'))



def load_keys():
    """Load the public and private key from the keys folder

    Returns:
        string: private and public key
    """
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey



if __name__ == "__main__":
    print("[+] Welcome to file encrypter and decrypter\n")
    print("[-] Please choose a folder to encrypt or decrypt")
    
    folder = open_folder()
    add_files_to_list(folder)
    print(f"[+] {len(files_list)} files found in {folder}\n")
    num_choice = input(f"{Fore.YELLOW}[+] What do you want to do?\n[1] Encrypt\n[2] Decrypt\n\n> ")
    try:
        num_choice = int(num_choice)
    except ValueError:
        num_choice = input(f"{Fore.YELLOW}[+] What do you want to do?\n[1] Encrypt\n[2] Decrypt\n\n> ")
     
    # Generate keys if they don't exist
    generate_keys()
    
    # Encrypt files
    if num_choice == 1:
        
        for f in files_list:
            with open(f, 'rb') as f:
                content = f.read()
            content_encrypted = encrypt(content, load_keys()[1])
            with open(f.name, 'wb') as f:
                f.write(content_encrypted)
                
        input(f"{Fore.GREEN}[+] Encryption completed. Press enter to exit...")
        quit()
        
    # Decrypt files
    elif num_choice == 2:
        count = 0
        
        for f in files_list:
            with open(f, 'rb') as f:
                content = f.read()
            content_decrypted = decrypt(content, load_keys()[0])
            if content_decrypted != False:
                with open(f.name, 'wb') as f:
                    f.write(content_decrypted)
                count+=1
        if count == len(files_list):
            input(f"{Fore.GREEN}[-] Decryption completed. Press enter to exit...")
            quit()
        print(f"{Fore.RED}[-] Some files could not be decrypted. Press enter to exit...")
        quit()
        
    else:
        input(f"{Fore.RED}[-] Invalid choice! Press enter to exit...")   
        quit() 
            