from lib import *


class RecieveFile(QMainWindow):


    def __init__(self) -> None:

        super().__init__()

        uic.loadUi(creating_path_to_ui_file("RecievingFile.ui"), self)

        self.ip_label = self.findChild(QLabel, "ip_label")
        self.ip_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.dir_label = self.findChild(QLabel, "dir_label")
        self.progress_label = self.findChild(QLabel, "progress_label")

        self.port_text_edit = self.findChild(QTextEdit, "port_text_edit")
        self.aes_text_edit = self.findChild(QTextEdit, "aes_texedit")

        self.set_server_button = self.findChild(QPushButton, "set_server")
        self.choose_dir_button = self.findChild(QPushButton, "choose_dir_button")
        self.save_file_button = self.findChild(QPushButton, "save_file_button")

        self.status_bar = self.findChild(QProgressBar, "saving_progress_bar")

        self.connection_status = self.findChild(QCheckBox, "conn_status_box")

        self.recv_server = RecieverSite()
        self.error_handler = Errorhandler()
        self.popup = PopupInfo()

        self.IP = self.recv_server.get_public_ip()
        self.PORT = None

        self.ip_label.setText(self.IP)


        self.choose_dir_button.clicked.connect(self.opening_file_dialog)
        self.set_server_button.clicked.connect(self.setting_up_server)
        self.save_file_button.clicked.connect(self.saving_file)

        self.recv_server.progress_signal.connect(self.updating_progress_bar_value)
        self.recv_server.progress_label_signal.connect(self.updating_progress_label_value)
        self.recv_server.recieving_finished.connect(self.close_and_popup)

    def close_and_popup(self, filename):
        
        self.close()
        self.popup.setting_labels("File has been recieved", filename)
        self.popup.show()


    def updating_progress_label_value(self, value: int, max_value: int):
        
        MB_value = round(float(value / 1048576), 2)
        max_MB_value = round(float(max_value / 1048576), 2)
        text = f'{MB_value} / {max_MB_value} MB'
        self.progress_label.setText(text)


    def updating_progress_bar_value(self, value: int):
        
        self.status_bar.setValue(value)


    def disabling_buttons(self):

        self.choose_dir_button.setEnabled(False)
        self.set_server_button.setEnabled(False)
        self.save_file_button.setEnabled(False)


    def opening_file_dialog(self):

        file_dialog = QFileDialog(self)
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


    def getting_cipher(self):

        key = self.aes_text_edit.toPlainText()

        if len(key) > 16:

            self.error_handler.error_handler("AES key should not be longer than 16 letters...")
            return False
        
        elif len(key) < 16:

            key = key + 'a' * (16-len(key))

        key = key.encode('utf-8')
        nonce = key
        self.cipher = AES.new(key, AES.MODE_EAX, nonce)

        return True


    def setting_up_server(self):

        self.PORT = self.port_text_edit.toPlainText()

        self. validity = self.getting_cipher()



        self.validity, error = self.recv_server.setting_server_addr(self.IP, self.PORT)

        if self.validity:

            self.connection_status.setStyleSheet("QCheckBox::indicator::unchecked {background-color:#00CC00 ;}")
        
        else:

            self.error_handler.error_handler(error)


    def saving_file(self):

        try:
            if self.validity is True and os.path.isdir(self.selected_dir):

                file_name, file_size = self.recv_server.file_acceptance()

                self.file_acceptance = FileAcceptance(self)

                acc_status = self.file_acceptance.getting_acceptance_satus(file_name, file_size)

                process = threading.Thread(target=self.recv_server.recieving_file, args=(self.selected_dir, file_name, file_size, self.cipher))

                if acc_status:
                    
                    

                    self.status_bar.setMinimum(0)
                    self.status_bar.setMaximum(file_size) 
                    self.status_bar.setValue(0)
                    
                    process.start()
                    self.disabling_buttons()
                    # self.connection_status.setStyleSheet("QCheckBox::indicator::unchecked {background-color:#00CC00 ;}")


                else:
                    
                    self.recv_server.break_connection()
            else:
                
                self.error_handler.error_handler("Please select proper directory or set valid server...")
        except:

            self.error_handler.error_handler("Please set valid server firstly...")


class FileAcceptance(QDialog):


    def __init__(self, parent = RecieveFile):

        super(FileAcceptance, self).__init__(parent)
        uic.loadUi(creating_path_to_ui_file("file_acceptance.ui"), self)
        
        self.file_name_label = self.findChild(QLabel, "file_name_label")
        self.file_size_label = self.findChild(QLabel, "file_size_label")

        self.dialog_options = self.findChild(QDialogButtonBox, "dialog_yes_no")

        self.dialog_options.accepted.connect(self.accept) 
        self.dialog_options.rejected.connect(self.reject) 


    def getting_acceptance_satus(self, file_label, file_size):
        
        self.file_name_label.setText(file_label)
        self.file_size_label.setText(str(f'{round(float(file_size / 1048576), 2)} MB'))
        result = self.exec()

        if result == QDialog.DialogCode.Accepted:

            return True
        
        else:

            return False

#TODO 
#Add progress bar pyqtsignal on reciever and sending site
#work on public IP sending option
#set windows to not be resizable
#Add popup window after file receiving 

