import json

DSIZE=102400
DELIMETER="<END_OF_RESULTS>"
def receive_file_folder(my_socket):
       print("[+] Receiving File/Folders")
       full_list=b''
       while True :
             chunk = my_socket.client_conn.recv(DSIZE)
             if chunk==(DELIMETER.encode('utf-8')):
                   break
             full_list=full_list+chunk
       
       print (" ")      
       file_dict=json.loads(full_list)
       for index in file_dict :
             print(f"[{index}] {file_dict[index]} ")                 
       
       print (" ")
       file_index=input("[+] Select File/Folder :")
       target = file_dict[file_index]
       my_socket.send_data(target)
       zipped_file=target+".zip"
       my_socket.receive_zipped(zipped_file)
       
             
      
       
                 
      