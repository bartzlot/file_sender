from lib import *


class RecieveFile(QMainWindow):


    def __init__(self) -> None:
        super().__init__()

        uic.loadUi(creating_path_to_ui_file("RecievingFile.ui"), self)

        

        self.ip_label = self.findChild(QLabel, "ip_label")
        self.dir_label = self.findChild(QLabel, "dir_label")

        self.port_text_edit = self.findChild(QTextEdit, "port_text_edit")

        self.set_server_button = self.findChild(QPushButton, "set_server")
        self.choose_dir_button = self.findChild(QPushButton, "choose_dir_button")
        self.save_file_button = self.findChild(QPushButton, "save_file_button")

        self.sending_progress_bar = self.findChild(QProgressBar, "saving_progress_bar")

        self.connection_status = self.findChild(QCheckBox, "conn_status_box")

        self.recv_server = RecieverSite()
        self.error_handler = Errorhandler()

        self.IP = self.recv_server.get_public_ip()
        self.PORT = None

        self.ip_label.setText(self.IP)

        self.choose_dir_button.clicked.connect(self.opening_file_dialog)
        self.set_server_button.clicked.connect(self.setting_up_server)


    def opening_file_dialog(self):

        file_dialog = QFileDialog()
        self.selected_dir = file_dialog.getExistingDirectory()
        self.dir_label.setText(self.selected_dir)
    

    def getting_public_ip_addr(self):

        try:
            response = requests.get("https://httpbin.org/ip")

            if response.status_code == 200:

                data = response.json()
                public_ip = data.get("origin")
                return public_ip
            
            else:
                return None
            
        except requests.RequestException:
            return None


    def setting_up_server(self):

        self.PORT = self.port_text_edit.toPlainText()

        self.validity, error = self.recv_server.setting_server_addr(self.IP, self.PORT)

        if self.validity:

            self.connection_status.setStyleSheet("QCheckBox::indicator::unchecked {background-color:#00CC00 ;}")
        
        else:

            self.error_handler.error_handler(error)


    def saving_file(self):

        if self.validity is True and os.path.isdir(self.selected_dir):

            self.recv_server.recieving_file(self.selected_dir)
        
        else:
            
            self.error_handler.error_handler("Please select proper directory or set valid server")


