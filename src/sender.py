from lib import *

class SenderSite(QMainWindow):

    sending_progress = pyqtSignal(int)
    sending_completed = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        
        self.IP = None
        self.PORT = None
        self.ADDR = None
        self.FORMAT = "utf-8"


    def setting_addr(self, ip, port):

        if port == '' or ip == '':
            return False, 'Port or IP text-box is empty...'
        
        elif not port.isnumeric():
            return False, "Port isn't numeric"
        
        self.IP = ip
        self.PORT = int(port)
        self.ADDR = (self.IP, self.PORT)

        try:

            self.creating_connection()

        except Exception as e:

            return False, e
        
        return True, ''
    

    def creating_connection(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


def sending_file(self, path: str, cipher):

    file_size = os.path.getsize(path)
    metadata = f"{os.path.basename(path)}\O{file_size}"

    self.client.sendall(metadata.encode('utf-8'))
    acknowledgement = self.client.recv(1024).decode('utf-8')

    if acknowledgement == "ACK":

        file_to_send = open(path, "rb")

        while True:

            chunk = file_to_send.read(32768)  

            if not chunk:
                
                break

            encrypted_chunk = cipher.encrypt(chunk)
            self.client.sendall(encrypted_chunk)

        self.client.send(b"<END>")
        self.client.close()
        self.sending_completed.emit(str(path))

    
    # def sending_file(self, path: str, cipher):

    #     try:

    #         file_size = os.path.getsize(path)

    #         metadata = f"{os.path.basename(path)}\O{file_size}"

    #         self.client.sendall(metadata.encode('utf-8'))

    #         acknowledgement = self.client.recv(1024).decode('utf-8')

    #         if acknowledgement == "ACK":


    #             file_to_send = open(path, "rb")
    #             data = file_to_send.read()

    #             encrypted_file = cipher.encrypt(data)

    #             self.client.sendall(encrypted_file)
                
    #             self.client.send(b"<END>")
    #             self.client.close()
                
    #             return True, ''

    #     except Exception as e:
            
    #         return False, e
