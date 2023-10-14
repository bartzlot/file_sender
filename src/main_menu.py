from lib import *


class MainMenu(QMainWindow):


    def __init__(self) -> None:
        super().__init__()

        uic.loadUi(creating_path_to_ui_file("MainMenu.ui"), self)

        self.send_file_button = self.findChild(QPushButton, "send_file_button")
        self.recv_file_button = self.findChild(QPushButton, "recv_file_button")
        self.quit_button = self.findChild(QPushButton, "quit_button")

        self.send_file_button.clicked.connect(self.send_file_button_event)
        self.recv_file_button.clicked.connect(self.recv_file_button_event)
        self.quit_button.clicked.connect(self.quit_button_event)


    def send_file_button_event(self):

        self.send_file = SendFile()
        self.send_file.show()


    def recv_file_button_event(self):

        self.recv_file = RecieveFile()
        self.recv_file.show()


    def quit_button_event(self):

        QApplication.quit()



    

app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())