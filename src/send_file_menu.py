from lib import *


class SendFile(QMainWindow):


    def __init__(self) -> None:
        super().__init__()

        uic.loadUi(creating_path_to_ui_file("SendingFile.ui"), self)
        
        self.validity = False

        self.ip_text_edit = self.findChild(QTextEdit, "ip_text_edit")
        self.port_text_edit = self.findChild(QTextEdit, "port_text_edit")

        self.set_connection_button = self.findChild(QPushButton, "set_conn_button")
        self.choose_dir_button = self.findChild(QPushButton, "choose_dir_button")
        self.send_file_button = self.findChild(QPushButton, "send_file_button")

        self.connection_status = self.findChild(QCheckBox, "conn_status_box")

        self.directory_label = self.findChild(QLabel, "dir_label")

        self.saving_progress_bar = self.findChild(QProgressBar, "sending_progress_bar")

        self.sender_client = SenderSite()
        self.error_handler = Errorhandler()

        self.set_connection_button.clicked.connect(self.setting_connection)
        self.choose_dir_button.clicked.connect(self.opening_file_dialog)
        self.send_file_button.clicked.connect(self.sending_file)

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

        if self.validity:

            self.connection_status.setStyleSheet("QCheckBox::indicator::unchecked {background-color:#00CC00 ;}")

        
        else:
            self.error_handler.error_handler(error)


    def sending_file(self):#TODO check if dir and connection is valid then send
        
        if self.validity is True and os.path.isfile(self.selected_file) == True:

            self.sender_client.sending_file(self.selected_file)
        
        else:

            self.error_handler.error_handler("Please select correct file or set proper connection...")