import socket
import os
import json


class SenderSite():


    def __init__(self) -> None:

        self.IP = self.get_public_ip()
        self.PORT = self.get_port()
        self.ADDR = (self.IP, self.PORT)
        self.PACKAGE_SIZE = 1024
        self.FORMAT = "utf-8"

        self.creating_connection()
        self. sending_file()
        
    def get_public_ip(self):

        ip = str(input("Please insert reciever IP address: "))

        return ip
        

    def get_port(self):

        port = int(input("Please insert open port: "))

        return port
    

    def creating_connection(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


    def sending_file(self):

        file_name = str(input("Please insert path or local filename to be send with file extension: "))
        file_size = os.path.getsize(file_name)

        metadata = {"file_name": file_name, "file_size": file_size}
        self.client.send(json.dumps(metadata).encode())

        file_to_send = open(file_name, "rb")
        data = file_to_send.read()

        self.client.sendall(data)
        self.client.send(b"<END>")
        self.client.close()
