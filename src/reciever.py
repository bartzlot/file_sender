from lib import *


class RecieverSite(QMainWindow):

    progress_signal = pyqtSignal(int)
    progress_label_signal = pyqtSignal(int, int)
    recieving_finished = pyqtSignal(str)

    def __init__(self) -> None:

        super().__init__()

        uic.loadUi(creating_path_to_ui_file("recv_file_status.ui"), self)

        self.status_bar = self.findChild(QProgressBar, 'saving_progress_bar')

        

        self.IP = None
        self.PORT = None
        self.ADDR = None
     
    def get_public_ip(self):
        """
        Get the public IP address of the server using a socket connection to a known server.

        Returns:
        - public_ip (str): The public IP address of the server.
        """        
        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            s.connect(("8.8.8.8", 80))
            
            public_ip = s.getsockname()[0]
            return public_ip
        
        except Exception as e:


            return None


    def get_port(self):
        """
        Prompt the user for an open port number for the server.

        Returns:
        - port (int): The user-entered port number.
        """
        port = int(input("Please insert open port: "))

        return port
    

    def setting_server_addr(self, ip: str, port: str):
        """
        Set the server's IP address and port.

        Parameters:
        - ip (str): The IP address.
        - port (str): The port number as a string.

        Returns:
        - validity (bool): True if the server is set up successfully, False otherwise.
        - error (str): An error message in case of failure.
        """
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


    def create_server(self, ADDR: set):
        """
        Create a server socket and bind it to the specified address.

        Parameters:
        - ADDR (set): A tuple representing the server's address (IP, PORT).
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
    

    def file_acceptance(self):
        """
        Accept the incoming file and extract its metadata.

        Returns:
        - recieved_file_name (str): The name of the received file.
        - recieved_file_size (int): The size of the received file in bytes.
        """
        self.server.listen()
        self.client, self.addr = self.server.accept()

        metadata = self.client.recv(1024).decode('utf-8')

        recieved_file_name, recieved_file_size = metadata.split('\O')
        recieved_file_size = int(recieved_file_size)        
        
        return recieved_file_name, recieved_file_size
    

    def break_connection(self):
        """
        Close the client socket to break the connection.
        """
        self.client.close()


    def recieving_file(self, dir_to_save: str, recieved_file_name: str, recieved_file_size: int, cipher, BUFFER_SIZE: int):
        """
        Receive and save the file to the specified directory.

        Parameters:
        - dir_to_save (str): The directory to save the received file.
        - recieved_file_name (str): The name of the received file.
        - recieved_file_size (int): The size of the received file in bytes.
        - cipher: An encryption object for decrypting the file.
        - BUFFER_SIZE (int): The size of the data buffer for receiving data.
        """
        dir = pathlib.Path(dir_to_save)
        recieved_file_name = dir.joinpath(recieved_file_name)

        file_to_save = open(recieved_file_name, "wb")
        file_to_save_bytes = b""
        done = False

        self.client.sendall("ACK".encode('utf-8'))
        
        
        while not done:
            
            data = self.client.recv(BUFFER_SIZE)
            
            if file_to_save_bytes[-5:] == b"<END>":

                done = True

            else:

                file_to_save_bytes += data
                self.progress_signal.emit(len(file_to_save_bytes))
                self.progress_label_signal.emit(len(file_to_save_bytes), recieved_file_size)
        
        decrypted_file = cipher.decrypt(file_to_save_bytes[:-5])
        
        file_to_save.write(decrypted_file)
        
        file_to_save.close()
        self.client.close()
        self.server.close()
        self.recieving_finished.emit(str(recieved_file_name))



