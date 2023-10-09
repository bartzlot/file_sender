import socket
import os
import json

def get_public_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Connect to a remote server (does not actually send any data)
        s.connect(("8.8.8.8", 80))
        
        # Get the local socket address, which includes the public IP
        public_ip = s.getsockname()[0]
        
        return public_ip
    except Exception as e:
        print(f"Error: {e}")
        return None

IP = str(input("Please insert reciever IP address: "))
PORT = int(input("Please insert open port: "))
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP, PORT))
print(IP)
file_name = "file.txt"
file_size = os.path.getsize("file.txt")

metadata = {"file_name": file_name, "file_size": file_size}
client.send(json.dumps(metadata).encode())

sfile = open("file.txt", "rb")
data = sfile.read()


client.sendall(data)
client.send(b"<END>")
client.close()