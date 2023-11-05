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

        # Additional Widgets
        self.header_table = QTableWidget()
        self.header_table.setColumnCount(2)
        self.header_table.setHorizontalHeaderLabels(["Header", "Value"])
        self.header_table.setColumnWidth(0, 150)
        self.header_table.setColumnWidth(1, 300)

        self.requestInfo = QPlainTextEdit()
        self.requestInfo.setTextInteractionFlags(Qt.NoTextInteraction)

        self.miscTabs.addTab(self.header_table, "HTTP Header")
        self.miscTabs.addTab(self.requestInfo, "Request Info")

        self.send_request(url)


    def send_request(self, url: str):
        self.header_table.setRowCount(0)
        self.requestInfo.clear()
        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)

    def handle_response(self, reply):
        if reply.error() == QNetworkReply.NoError:
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            self.requestInfo.appendPlainText(f"HTTP Status Code: {status_code}")

            headers = reply.rawHeaderList()
            for header in headers:
                header_cell = QTableWidgetItem(header.data().decode("utf-8"))
                value_cell = QTableWidgetItem(reply.rawHeader(header).data().decode("utf-8"))

                self.header_table.insertRow(self.header_table.rowCount())
                self.header_table.setItem(self.header_table.rowCount() - 1, 0, header_cell)
                self.header_table.setItem(self.header_table.rowCount() - 1, 1, value_cell)

            content = reply.readAll().data()
            self.setEditorData([b for b in content])

        else:
            self.requestInfo.appendPlainText("Error: " + reply.errorString())

    @override
    def saveData(self):
        super().saveDataAs()