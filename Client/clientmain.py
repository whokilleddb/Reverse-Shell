from Client import *
from clientconnectionhandler import *

my_socket=ClientConnection()
ip = "127.0.0.1"
port = 8080
my_socket.CreateConnection(ip,port)
print(f"[+]Connecting To Server at {ip} On Port {port}")
print(my_socket.recv_data())
my_socket.send_data("[+] CONNECTED TO CLIENT")
clienthandler(my_socket)
print("[+] Exiting Client")
my_socket.end_conn()