def checkpass(my_socket):
     i=0
     counter = 0
     while i<3 :
         val = my_socket.recv_data()
         if val == "11fcb6aa20f1226678e8cc5cbdf8f29f94b4a6a8":
             #Password Hash for "whokilleddb" 
             #Generate your own password hash using hashgenerator.py and replace the given hash 
             my_socket.send_data("[+] Okay")
             counter=1 
             break
         else :
             my_socket.send_data("[+] Wrong Password")
         
         i=i+1     
              
     return counter
