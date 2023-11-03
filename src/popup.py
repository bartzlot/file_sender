from lib import *

class PopupInfo(QWidget):

    def __init__(self) -> None:

        super().__init__()
        uic.loadUi(creating_path_to_ui_file("info_dialog.ui"), self)

        self.info_label = self.findChild(QLabel, "info_label")
        self.dir_label = self.findChild(QLabel, "file_dir")

        self.confirm_button = self.findChild(QPushButton, "confirm_button")

        self.confirm_button.clicked.connect(self.confirm_button_event)

    def confirm_button_event(self):
        """
        Handle the confirm button click event by closing the dialog.
        """
        self.close()


    def setting_labels(self, info: str, path: str):
        """
        Set the text for info_label and dir_label, and display the dialog.

        Parameters:
        - info (str): Information text to display.
        - path (str): File path to display.
        """
        self.info_label.setText(info)
        self.dir_label.setText(str(path))
        self.show()