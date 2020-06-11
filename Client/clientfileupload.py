from glob import glob
import json
DSIZE=102400
DELIMITER="<END_OF_RESULTS>"
def upload_file_folder(my_socket):
     print("[+] Uploading File/Folder To Server")
     files= glob("*")
     dict = {}
     for index , file in enumerate(files):
         dict[index]=file
         
     dict_bytes=json.dumps(dict)
     raw_bytes = dict_bytes.encode('utf-8')
     while True:
             my_socket.socket.send(raw_bytes[:DSIZE])
             raw_bytes=raw_bytes[DSIZE:]
             if raw_bytes==b'':
                  my_socket.socket.send(DELIMITER.encode('utf-8'))
                  break
          
     
     
     filetosend=my_socket.recv_data()
     my_socket.send_file(filetosend)
     