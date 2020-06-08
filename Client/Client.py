import socket

DSIZE = 102400 #Data Size
DELIMETER = "<END_OF_RESULTS>"

class ClientConnection :
     def __init__(self):
        """Create TCP Socket
        """
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
     def CreateConnection(self , server_ip , server_port) :
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket.connect((server_ip , server_port))
         
     def send_data(self,data):
        self.bytedata = data.encode('utf-8')
        self.socket.send(self.bytedata)
        
     def recv_data(self):
        self.bytedata = self.socket.recv(DSIZE)
        self.data = self.bytedata.decode('utf-8')
        return self.data
    
     def receive_command_result(self):
         print("[+] Getting Command Results")
         result = b''
         while True:
             chunk = self.socket.recv(DSIZE)
             if chunk.endswith(DELIMETER.encode()):
                chunk += chunk[:-len(DELIMETER)]
                result += chunk
                break
             result += chunk
         self.data = result.decode()
         return (result.decode())    
        
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

     def recv_file(self, filename):
         print(f"[+] Receive {filename}")
         filename="New"+filename
         with open(filename,'wb') as file:
             while True:
                 chunk = self.socket.recv(DSIZE)
                 if chunk.endswith(DELIMETER.encode()):
                     chunk=chunk[:-len(DELIMETER)]
                     file.write(chunk)
                     break
                 file.write(chunk)
                 
         print("[+] Completed")             

     def end_conn(self):
        self.socket.close()
    