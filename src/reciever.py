from lib import *


class RecieverSite(QMainWindow):

    progress_signal = pyqtSignal(int)
    progress_label_signal = pyqtSignal(int, int)
    recieving_finished = pyqtSignal()

    def __init__(self) -> None:

        super().__init__()

        uic.loadUi(creating_path_to_ui_file("recv_file_status.ui"), self)

        self.status_bar = self.findChild(QProgressBar, 'saving_progress_bar')

        

        self.IP = None
        self.PORT = None
        self.ADDR = None
        self.popup = PopupInfo()
     
    def get_public_ip(self):
        
        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            s.connect(("8.8.8.8", 80))
            
            public_ip = s.getsockname()[0]
            return public_ip
        
        except Exception as e:


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
    

    def file_acceptance(self):

        self.server.listen()
        self.client, self.addr = self.server.accept()

        metadata = self.client.recv(1024).decode('utf-8')

        recieved_file_name, recieved_file_size = metadata.split('\O')
        recieved_file_size = int(recieved_file_size)        
        
        return recieved_file_name, recieved_file_size
    
    def break_connection(self):
        
        self.client.close()


    def recieving_file(self, dir_to_save, recieved_file_name, recieved_file_size, cipher):

        # self.server.listen()
        # self.client, self.addr = self.server.accept()

        # metadata = self.client.recv(1024).decode('utf-8')

        # recieved_file_name, recieved_file_size = metadata.split('\O')
        # recieved_file_size = int(recieved_file_size)
        # print(recieved_file_name, recieved_file_size)
        # metadata = json.loads(self.client.recv(1024).decode('utf-8'))
        # recieved_file_name = metadata["file_name"]
        # recieved_file_size = metadata["file_size"]
        
        # acceptance_sig = pyqtSignal.emit(str, int)
        # acceptance_sig.emit(recieved_file_name, recieved_file_size)

        bar_value_update = 0   



        dir = pathlib.Path(dir_to_save)
        recieved_file_name = dir.joinpath(recieved_file_name)

        file_to_save = open(recieved_file_name, "wb")
        file_to_save_bytes = b""
        done = False

        self.client.sendall("ACK".encode('utf-8'))

        while not done:

            data = self.client.recv(32768)

            bar_value_update += 32768

            self.progress_signal.emit(bar_value_update)
            self.progress_label_signal.emit(bar_value_update, recieved_file_size)

            if file_to_save_bytes[-5:] == b"<END>":
                done = True

            else:
                file_to_save_bytes += data

        decrypted_file = cipher.decrypt(file_to_save_bytes[:-5])
        
        file_to_save.write(decrypted_file)
        
        file_to_save.close()
        self.client.close()
        self.server.close()
        self.recieving_finished.emit()
        self.popup.setting_labels("File has been recieved", recieved_file_name)
        self.popup.show()


