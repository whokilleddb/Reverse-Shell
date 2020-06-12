def capture_screenshot(my_socket):
         print("[+] Capturing Screenshot")
         zipped_name="screenshot.zip"
         my_socket.receive_zipped(zipped_name)