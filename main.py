import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("home.ui", self)
        self.downloadButton.clicked.connect(self.download)
        self.show()

    def download(self):
        link = self.linkInputField.text()

        # Start the download process
        self.promptUser.setText("التقدم: 0%")
        self.download = DownloadThread(link)
        self.download.progress_signal.connect(self.update_progress)
        self.download.start()

    def update_progress(self, progress):
        self.promptUser.setText(f"التقدم: {progress}%")
        if self.promptUser.text() == "التقدم: 100%":
            self.show_finished_screen()

    def show_finished_screen(self):
        self.promptUser.setText("تم التحميل")
        self.linkInputField.setText("")


class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, link):
        super(DownloadThread, self).__init__()
        self.link = link

    def run(self):
        try:
            user_name = os.getlogin()
            yt = YouTube(self.link, on_progress_callback=self.on_progress)
            vid_stream = yt.streams.get_highest_resolution()
            vid_stream.download(f"C:\\Users\\{user_name}\\Downloads")
        except:
            print(f"An error occurred in the download function")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        downloaded_bytes = total_size - bytes_remaining
        progress = int(downloaded_bytes / total_size * 100)
        self.progress_signal.emit(progress)

# Initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
