import sys
import os
import pathlib
import requests
import socket
from PyQt6.QtWidgets import (QWidget, QApplication, 
                             QMainWindow, QCalendarWidget, 
                             QDateEdit, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem,
                             QDialog, QTextEdit, QDialogButtonBox,
                             QFileDialog, QCheckBox, QComboBox, QProgressBar)

from PyQt6.QtGui import (QPalette, QTextCharFormat, 
                         QColor, QPainter, QCloseEvent, QPixmap
                         , QIcon)

from PyQt6.QtCore import (Qt, QDate, QDateTime, 
                          QRect, QPoint, pyqtSignal)
from PyQt6 import QtCore, uic

from utilities import creating_path_to_ui_file, Errorhandler
from sender import SenderSite
from reciever import RecieverSite
from send_file_menu import SendFile
from recieve_file_menu import RecieveFile
from main_menu import MainMenu
