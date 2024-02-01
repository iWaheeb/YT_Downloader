import sys
import os

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5 import uic
from pytube import YouTube

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("home.ui", self)

        # Define widgets
        self.prompt_user = self.findChild(QLabel, "promptUser")
        self.link_input_field = self.findChild(QLineEdit, "linkInputField")
        self.download_button = self.findChild(QPushButton, "downloadButton")

        # actions
        self.download_button.clicked.connect(self.download)

        self.show()

    def download(self):
        try:
            self.user_name = os.getlogin()
            self.link = self.link_input_field.text()
            yt = YouTube(self.link)
            vid_stream = yt.streams.get_highest_resolution()
            vid_stream.download(f"C:\\Users\\{self.user_name}\\Downloads")

        except:
            print("An error occured in the download function")

# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()