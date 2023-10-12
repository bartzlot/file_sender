import socket
import json


class ServerSite():
    

    def __init__(self) -> None:

        self.IP = self.get_public_ip()
        print(self.IP)
        self.PORT = self.get_port()
        self.create_server()
        self.recieving_file()
     
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
    

    def create_server(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.IP, self.PORT))

    
    def recieving_file(self):

        self.server.listen()
        self.client, self.addr = self.server.accept()

        metadata = json.loads(self.client.recv(1024).decode())
        recieved_file_name = metadata["file_name"]
        recieved_file_size = metadata["file_size"]

        saved_file_name = str(input("Please insert file name with correct file extension to save: "))

        file_to_save = open(saved_file_name, "wb")
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

server = ServerSite()