# https://raw.githubusercontent.com/AsayuGit/FooCalcRPL/main/src/CalcServer.java

from Hexeditor import Hexeditor

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from overrides import override

class NetworkHexEditor(Hexeditor):
    def __init__(self, url: str):
        super().__init__()

        self.fileURL = url

        # Load data
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_response)

        self.send_request(url)


    def send_request(self, url: str):
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)

    def handle_response(self, reply):
        if reply.error() == QNetworkReply.NoError:
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            print(f"HTTP Status Code: {status_code}")

            content = reply.readAll().data()
            self.setEditorData([b for b in content])
        else:
            print("Error: " + reply.errorString())

    @override
    def saveData(self):
        super().saveDataAs()