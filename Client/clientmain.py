from Client import *
from clientconnectionhandler import *
from check import *


my_socket=ClientConnection()
ip = "127.0.0.1"
port = 8080



my_socket.CreateConnection(ip,port)
print(f"[+]Connecting To Server at {ip} On Port {port}")
print(my_socket.recv_data())


print ("[+] Checking Password.")
counter  = checkpass(my_socket)

if counter == 1:
      my_socket.send_data("[+] Authentication Successful")
      my_socket.send_data("[+] Connected To Client")
      clienthandler(my_socket)
      print("[+] Exiting Client")
      my_socket.end_conn()
     
else :
      print("[+] Authentication Error")
      my_socket.end_conn()