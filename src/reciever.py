from lib import *


class RecieverSite(QMainWindow):
    

    def __init__(self) -> None:

        super().__init__()

        uic.loadUi(creating_path_to_ui_file("recv_file_status.ui"), self)

        self.status_bar = self.findChild(QProgressBar, 'saving_progress_bar')

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
        print("server binded")
    

    def file_acceptance(self):

        self.server.listen()
        self.client, self.addr = self.server.accept()

        
        

    
    def break_connection(self):
        
        self.client.close()


    def recieving_file(self, dir_to_save):

        self.server.listen()
        self.client, self.addr = self.server.accept()

        metadata_json = self.client.recv(1024).decode('utf-8')
        metadata = json.loads(metadata_json)
        recieved_file_name = metadata["file_name"]
        recieved_file_size = metadata["file_size"]
        print(recieved_file_name, recieved_file_size)
        # metadata = json.loads(self.client.recv(1024).decode('utf-8'))
        # recieved_file_name = metadata["file_name"]
        # recieved_file_size = metadata["file_size"]
        
        # acceptance_sig = pyqtSignal.emit(str, int)
        # acceptance_sig.emit(recieved_file_name, recieved_file_size)
        
        bar_value_update = 0   
        self.status_bar.setMinimum(0)
        self.status_bar.setMaximum(recieved_file_size) 
        self.status_bar.setValue(bar_value_update)
        self.show()
        
        dir = pathlib.Path(dir_to_save)
        recieved_file_name = dir.joinpath("test.txt")

        file_to_save = open(recieved_file_name, "wb")
        file_to_save_bytes = b""
        done = False

        while not done:

            data = self.client.recv(1024)

            bar_value_update += 1024
            self.status_bar.setValue(bar_value_update)

            if file_to_save_bytes[-5:] == b"<END>":
                done = True

            else:
                file_to_save_bytes += data

        file_to_save.write(file_to_save_bytes[:-5])
        file_to_save.close()
        self.client.close()
        self.server.close()
        self.close()
        print("file recieved")


