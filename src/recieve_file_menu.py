from lib import *


class RecieveFile(QMainWindow):


    def __init__(self) -> None:
        super().__init__()

        uic.loadUi(creating_path_to_ui_file("RecieveFile.ui"), self)

        self.ip_text_edit = self.findChild(QTextEdit, "ip_text_edit")
        self.port_text_edit = self.findChild(QTextEdit, "port_text_edit")

        self.set_connection_button = self.findChild(QPushButton, "set_conn_button")
        self.choose_dir_button = self.findChild(QPushButton, "choose_dir_button")
        self.save_file_button = self.findChild(QPushButton, "save_file_button")

        self.connection_status = self.findChild(QCheckBox, "conn_status_box")

        self.directory_label = self.findChild(QLabel, "dir_label")

        self.saving_progress_bar = self.findChild(QProgressBar, "saving_progress_bar")