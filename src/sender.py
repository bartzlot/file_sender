from lib import *

class SenderSite():


    def __init__(self) -> None:

        self.IP = None
        self.PORT = None
        self.ADDR = None
        self.PACKAGE_SIZE = 1024
        self.FORMAT = "utf-8"

        # self.creating_connection()
        # self. sending_file()
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

            print(f'An error has occured: {e}')
            return False, e
        
        return True, ''
    

    def creating_connection(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


    def sending_file(self, path: str):

        file_size = os.path.getsize(path)

        metadata = {"file_name": os.path.basename(path), "file_size": file_size}
        self.client.send(json.dumps(metadata).encode())

        file_to_send = open(path, "rb")
        data = file_to_send.read()

        self.client.sendall(data)
        self.client.send(b"<END>")
        self.client.close()