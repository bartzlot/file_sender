import socket
import json


class RecieverSite():
    

    def __init__(self) -> None:

        self.IP = None
        self.PORT = None
        self.ADDR = None
     
    def get_public_ip(self):
        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            s.connect(("8.8.8.8", 80))
            
            public_ip = s.getsockname()[0]
            print(public_ip)
            return public_ip
        
        except Exception as e:

            print(f"Error: {e}")

            return None


    def get_port(self):

        port = int(input("Please insert open port: "))

        return port
    

    def setting_server_addr(self, ip, port):

        if port == '' or ip == '':
            return False, 'Port or IP text-box is empty...'
        
        elif not port.isnumeric():
            return False, "Port isn't numeric"
        
        self.IP = ip
        self.PORT = int(port)
        self.ADDR = (self.IP, self.PORT)

        try:
            
            self.create_server(self.ADDR)
        
        except Exception as e:

            return False, e

        return True, ''

    def create_server(self, ADDR):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
    

    
    def recieving_file(self, dir_to_save):

        self.server.listen()
        self.client, self.addr = self.server.accept()

        metadata = json.loads(self.client.recv(1024).decode())
        recieved_file_name = metadata["file_name"]
        recieved_file_size = metadata["file_size"]


        saved_file_name = str(input("Please insert file name with correct file extension to save: "))

        recieved_file_name = dir_to_save + saved_file_name

        file_to_save = open(recieved_file_name, "wb")
        file_to_save_bytes = b""
        done = False

        while not done:

            data = self.client.recv(1024)

            if file_to_save_bytes[-5:] == b"<END>":
                done = True

            else:
                file_to_save_bytes += data

        file_to_save.write(file_to_save_bytes[:-5])
        file_to_save.close()
        self.client.close()
        self.server.close()


