from lib import *
def creating_path_to_ui_file(filename: str):

    file_path = pathlib.PurePath(__file__)
    file_path = file_path.parent.parent
    file_path = file_path.joinpath('ui', filename)

    return str(file_path)


class Errorhandler(QDialog):


    def __init__(self, parent = None):

        super(Errorhandler, self).__init__(parent)
        uic.loadUi(creating_path_to_ui_file('ErrorDialog.ui'), self)

        self.error_text_label = self.findChild(QLabel, "error_text_label")
        self.ok_button = self.findChild(QPushButton, "ok_button")

        self.ok_button.clicked.connect(self.ok_button_event)


    def error_handler(self, error_mess):
        """Error window with specified error message

        Args:
            error_mess (str, error): error message displayed in window
        """
        self.error_text_label.setText(str(error_mess))
        self.show()


    def ok_button_event(self):
        self.close()


