from lib import *


class RecieveFile(QMainWindow):


    def __init__(self) -> None:
        super().__init__()

        uic.loadUi(creating_path_to_ui_file("RecievingFile.ui"), self)

        # self.ip_label = self.findChild(QLabel, "ip_label")

        # self.port_text_edit = self.findChild(QTextEdit, "port_text_edit")

        # self.set_server_button = self.findChild(QPushButton, "set_server")
        # self.choose_file_button = self.findChild(QPushButton, "choose_dir_button")
        # self.send_file_button = self.findChild(QPushButton, "send_file_button")

        # self.sending_progress_bar = self.findChild(QProgressBar, "sending_progress_bar")

        # self.connection_status = self.findChild(QCheckBox, "conn_status_box")


        