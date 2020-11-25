from urllib import request
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import Qt
from configparser import ConfigParser
from os import remove


def check_version(remote_url: str, local_url, download_url: str):
    try:
        request.urlretrieve(remote_url, 'remote_version.txt')
    except ValueError:
        print('Invalid Url')

    try:
        with open(local_url, 'r') as local_f:
            local_version = float(local_f.read())
            with open('remote_version.txt', 'r') as remote_f:
                remote_version = float(remote_f.read())
                if remote_version > local_version:
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("New version avalible")
                    msg_box.setTextFormat(Qt.RichText)
                    msg_box.setText("A new version avalible! \n"
                                    f"<a href='{download_url}'>\nDownload now</a>")
                    msg_box.exec()
            remove('remote_version.txt')
    except FileNotFoundError:
        print('Local file not found')


def load_settings():
    config: ConfigParser = ConfigParser()
    config.optionxform = str
    try:
        settings = open("settings.ini", "r")
        settings.close()
        config.read("settings.ini")
    except FileNotFoundError:
        config["Urls"] = {'RemoteFile': '',
                          'LocalFile': '',
                          'DownloadLink': ''
                          }
        with open('settings.ini', 'w') as file:
            config.write(file)

    urls = config['Urls']
    return urls['RemoteFile'], urls['LocalFile'], urls['DownloadLink']


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    r, l, d = load_settings()
    check_version(r, l, d)
