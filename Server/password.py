import hashlib

def check_password(my_socket):
     i= 0
     counter = 0
     print("[+] Authenticate Yourself")
     while i<3:
         opt = 3-i
         print(f"[+] {opt} Chance Remaining")
         password = input("[+] Enter Password : ")
         passbytes = password.encode('utf-8')
         hashval = hashlib.sha1(passbytes).hexdigest()
         checksum = str(hashval)
         my_socket.send_data(checksum)
         counter = my_socket.recv_data()
         if counter == "[+] Okay":
             print("[+] Daddy's Home")
             counter = 1
             break
         else :
             print("[+] Wrong One Kiddo")
         i=i+1
     return counter
