def checkpass(my_socket):
     val = my_socket.recv_data()
     if val == "11fcb6aa20f1226678e8cc5cbdf8f29f94b4a6a8":
         my_socket.send_data("[+] Okay")
         return 1 
         
     else :
         my_socket.send_data("[+] Wrong Password")
         return 0