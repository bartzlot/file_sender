from lib import *


class SendFile(QMainWindow):


    def __init__(self) -> None:
        super().__init__()

        uic.loadUi(creating_path_to_ui_file("SendingFile.ui"), self)

        self.validity = False

        self.progress_label = self.findChild(QLabel, "progress_label")

        self.ip_text_edit = self.findChild(QTextEdit, "ip_text_edit")
        self.port_text_edit = self.findChild(QTextEdit, "port_text_edit")

        self.set_connection_button = self.findChild(QPushButton, "set_conn_button")
        self.choose_dir_button = self.findChild(QPushButton, "choose_dir_button")
        self.send_file_button = self.findChild(QPushButton, "send_file_button")

        self.connection_status = self.findChild(QCheckBox, "conn_status_box")

        self.directory_label = self.findChild(QLabel, "dir_label")
        self.aes_textedit = self.findChild(QTextEdit, "aes_textedit")

        self.sending_progress_bar = self.findChild(QProgressBar, "sending_progress_bar")

        self.sender_client = SenderSite()
        self.error_handler = Errorhandler()
        self.popup = PopupInfo()

        self.set_connection_button.clicked.connect(self.setting_connection)
        self.choose_dir_button.clicked.connect(self.opening_file_dialog)
        self.send_file_button.clicked.connect(self.sending_file)

        self.sender_client.sending_progress.connect(self.updating_progress_bar)
        self.sender_client.sending_completed.connect(self.close_and_popup)
        self.sender_client.sending_progress_values.connect(self.updating_progress_label_value)

    def updating_progress_bar(self, value: int):

        self.sending_progress_bar.setValue(value)


    def close_and_popup(self, filename):
        
        self.close()
        self.popup.setting_labels("File has been recieved", filename)
        self.popup.show()


    def disabling_buttons(self):

        self.set_connection_button.setEnabled(False)
        self.choose_dir_button.setEnabled(False)
        self.send_file_button.setEnabled(False)


    def updating_progress_label_value(self, value: int, max_value: int):
        
        MB_value = round(float(value / 1048576), 2)
        max_MB_value = round(float(max_value / 1048576), 2)
        text = f'{MB_value} / {max_MB_value} MB'
        self.progress_label.setText(text)


    def generating_aes_key(self):


        key = self.aes_textedit.toPlainText()

        if len(key) > 16:

            self.error_handler.error_handler("AES key should not be longer than 16 letters...")
            return False
        
        elif len(key) < 16:

            key = key + 'a' * (16-len(key))
        
        key = key.encode('utf-8')
        nonce = key
        self.cipher = AES.new(key, AES.MODE_EAX, nonce)

        return True


    def opening_file_dialog(self):

        file_dialog = QFileDialog()
        file_dialog.setNameFilter("All Files (*)")
        self.selected_file = file_dialog.getOpenFileName(None, "Open File", "", "All Files (*)")
        self.selected_file = self.selected_file[0]
        self.directory_label.setText(self.selected_file)


    def setting_connection(self):

        ip = self.ip_text_edit.toPlainText()
        port = self.port_text_edit.toPlainText()

        self.validity, error = self.sender_client.setting_addr(ip, port)

        if self.validity and self.generating_aes_key():

            self.connection_status.setStyleSheet("QCheckBox::indicator::unchecked {background-color:#00CC00 ;}")

        else:

            self.error_handler.error_handler(error)


    def sending_file(self):

        try:

            if self.validity is True and os.path.isfile(self.selected_file) == True:

                self.sending_progress_bar.setMinimum(0)
                self.sending_progress_bar.setMaximum(os.path.getsize(self.selected_file))
                process = threading.Thread(target=self.sender_client.sending_file, args=(self.selected_file, self.cipher))
                process.start()
                self.disabling_buttons()
            else:

                self.error_handler.error_handler("Please select correct file or set proper connection...")
        
        except:

            self.error_handler.error_handler("Sending file has been terminated by server...")