import socket
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

IP = get_public_ip()
PORT = int(input("Please insert open port: "))

print(IP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))
    
server.listen()

client, addr = server.accept()

metadata = json.loads(client.recv(1024).decode())

file_name = metadata["file_name"]
file_size = metadata["file_size"]

print(file_name)
print(file_size)

file = open("e.txt", "wb")

done = False

file_bytes = b""

# progress = tqdm.tqdm(unit="B", unit_scale=True, 
#                      unit_divisor=1024, total=int(file_size))

while not done:

    data = client.recv(1024)

    if file_bytes[-5:] == b"<END>":
        done = True
    else:
        file_bytes += data
        # progress.update(1024)

file.write(file_bytes[:-5])

file.close()
client.close()
server.close()