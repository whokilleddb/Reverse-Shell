from glob import glob
import os

def upload_file(my_socket):
     print ("[+] File List ")
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
            
     print("[+] File Selected = " , filetosend)
     my_socket.send_data(filetosend)
     my_socket.send_file(filetosend)