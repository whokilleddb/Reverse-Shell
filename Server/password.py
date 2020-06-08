import hashlib

def check_password(my_socket):
     password = input("[+] Enter Password : ")
     passbytes = password.encode('utf-8')
     hashval = hashlib.sha1(passbytes).hexdigest()
     checksum = str(hashval)
     my_socket.send_data(checksum)
     counter = my_socket.recv_data()
     if counter == "[+] Okay":
         print("[+] Daddy's Home")
         return 1
     else :
         print("[+] Wrong One Kiddo")
         return 0