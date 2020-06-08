import socket

DSIZE = 102400 #Data Size
DELIMETER = "<END_OF_RESULTS>"

class ServerConnection :
    def __init__(self):
        """Create TCP Socket
        """
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    def CreateConnection(self  , port) :
        self.server_ip = "127.0.0.1"
        self.server_port = port
        
        self.socket.bind((self.server_ip,self.server_port))
    
    def Listen(self , noc): #noc = Number Of Connections
        self.socket.listen(noc)
        
    def AcceptConnection(self):
        self.client_conn , self.client_add = self.socket.accept()
        return (self.client_conn , self.client_add)
    
    def send_data(self , cmd):
        self.client_conn.send(cmd.encode('utf-8'))
        
    def recv_data(self):
        data = self.client_conn.recv(DSIZE)
        self.data = data.decode('utf-8')
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
    
    def end_conn(self):
        self.client_conn.close()
        self.socket.close()
        