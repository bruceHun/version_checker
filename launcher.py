from urllib import request, error
from PyQt5.QtWidgets import QMessageBox, QApplication
from configparser import ConfigParser
from os import remove, system, path, chdir


def check_version(remote_url: str, local_url, download_url: str, app_title: str):
    try:
        request.urlretrieve(remote_url, 'remote_versions.ini')
    except ValueError:
        print('Invalid Url')
    except error.URLError:
        print('Invalid URL')
        return

    try:
        with open(local_url, 'r') as local_f:
            local_version = float(local_f.read())
            with open('remote_versions.ini', 'r') as remote_f:
                # remote_version = float(remote_f.read())
                config: ConfigParser = ConfigParser()
                config.optionxform = str
                config.read("remote_versions.ini")
                remote_version = float(config[app_title]['version'])
                # print(f'r_v: {remote_version}, l_v: {local_version}')
                if remote_version > local_version:
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("New version avalible")
                    # Qt.RichText == 1
                    msg_box.setTextFormat(1)
                    msg_box.setText("A new version avalible! \n"
                                    f"<a href='{download_url}'>\nDownload now</a>")
                    msg_box.exec()
            remove('remote_versions.ini')
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
        config["TargetAPP"] = {'Title': '',
                               'Path': ''}
        with open('settings.ini', 'w') as file:
            config.write(file)

    urls = config["Urls"]
    tgt = config["TargetAPP"]
    return urls['RemoteFile'], urls['LocalFile'], urls['DownloadLink'], tgt['Title'], tgt['Path']


def run_app(_path: str):
    directory = path.dirname(_path)
    chdir(directory)
    return system(path.basename(_path))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    r, l, d, t, p = load_settings()
    check_version(r, l, d, t)
    print(f"exit with code {run_app(p)}")
