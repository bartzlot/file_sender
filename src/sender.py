from lib import *

class SenderSite(QMainWindow):

    sending_progress = pyqtSignal(int)
    sending_completed = pyqtSignal(str)
    sending_progress_values = pyqtSignal(int, int)

    def __init__(self) -> None:
        super().__init__()
        
        self.IP = None
        self.PORT = None
        self.ADDR = None
        self.FORMAT = "utf-8"


    def setting_addr(self, ip: str, port: str):
        """
        Set the server's IP address and port for communication.

        Parameters:
        - ip (str): The server's IP address.
        - port (str): The server's port number.

        Returns:
        - tuple (bool, str): A tuple indicating if the address is set and an error message if not.
        """
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
        """
        Create a socket connection to the server using the stored IP and PORT attributes.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


    def sending_file(self, path: str, cipher, BUFFER_SIZE: int):
        """
        Send a file to the server.

        Parameters:
        - path (str): The path to the file to be sent.
        - cipher: The AES encryption object for secure file transmission.
        - BUFFER_SIZE (int): The size of the data chunks to be sent.

        Emits:
        - sending_progress: The sending progress in bytes.
        - sending_completed: Indicates that file sending is completed.
        - sending_progress_values: The sending progress in bytes and total file size.
        """
        file_size = os.path.getsize(path)
        metadata = f"{os.path.basename(path)}\O{file_size}"

        self.client.sendall(metadata.encode('utf-8'))

        acknowledgement = self.client.recv(1024).decode('utf-8')

        already_sent_bytes_amount = 0
        if acknowledgement == "ACK":

            file_to_send = open(path, "rb")

            while True:

                chunk = file_to_send.read(BUFFER_SIZE)  
                
                if not chunk:
                    
                    break
                    
                encrypted_chunk = cipher.encrypt(chunk)
                self.client.sendall(encrypted_chunk)
                already_sent_bytes_amount += BUFFER_SIZE
                self.sending_progress.emit(already_sent_bytes_amount)
                self.sending_progress_values.emit(already_sent_bytes_amount, file_size)

            self.client.send(b"<END>")
            self.client.close()
            self.sending_completed.emit(str(path))

