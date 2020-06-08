from Server import *
from serverconnectionhandler import *
import hashlib
from password import *

my_socket = ServerConnection()
port = 8080
my_socket.CreateConnection(port)
print(f"[+] Creating Socket And Binding It To Port {port}")
my_socket.Listen(3)
print("[+] Socket Is Listening For Connections")
my_conn , addr= my_socket.AcceptConnection()
print(f"[+] Connected To {addr[0]} On Port {addr[1]}")
my_socket.send_data("[+] Success")
flagval = check_password(my_socket)
if flagval == 1 :
     print(my_socket.recv_data())
     serverhandler(my_socket)
     print("[+] Exiting Server")
     my_socket.end_conn()

else :
     print ("[+] Closing Connection")
     my_socket.end_conn()