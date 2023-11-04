from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from Hexwidget import Hexwidget
from Textwidget import Textwidget

class Hexeditor(QWidget):
    def __init__(self, path: str):
        super().__init__()

        self.filePath = path

        # Layouts
        layout = QVBoxLayout()
        topLayout = QHBoxLayout()

        # Initial Setup
        file = open(path, "rb")
        self.data = [b for b in file.read()]
        file.close()

        # Child Widgets
        self.hexwidget = Hexwidget(self)
        self.textarea = Textwidget(self)
        self.miscTabs = QTabWidget(self)
        self.miscTabs.addTab(QWidget(), "Temp")
        self.miscTabs.addTab(QWidget(), "Temp2")

        # Dialogs
        self.saveFileDialog = QFileDialog(self)
        self.saveFileDialog.setFileMode(QFileDialog.AnyFile)
        self.saveFileDialog.setWindowTitle("Save File As...")
        self.saveFileDialog.setAcceptMode(QFileDialog.AcceptSave)
        self.saveFileDialog.fileSelected.connect(self.doSaveFileAs)

        # Widgets Settings
        self.textarea.setCursorCoordinates(0, 0)
        self.hexwidget.setCursorCoordinates(0, 0)

        self.hexwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Event Connections
        self.hexwidget.indexChanged.connect(self.notifyCursorPosToText)
        self.textarea.indexChanged.connect(self.notifyCursorPosToHex)
        
        self.hexwidget.verticalScrollBar().valueChanged.connect(self.notifyScrollPosToText)
        self.textarea.verticalScrollBar().valueChanged.connect(self.notifyScrollPosToHex)
        
        # Layout Setup
        topLayout.addWidget(self.hexwidget)
        topLayout.addWidget(self.textarea)

        layout.addLayout(topLayout)
        layout.addWidget(self.miscTabs)
        self.setLayout(layout)

    def saveData(self):
        saveFile = open(self.filePath, "wb")
        saveFile.write(bytearray(self.data))
        saveFile.close()

    def saveDataAs(self):
        self.saveFileDialog.open()

    def doSaveFileAs(self, file: str):
        saveFile = open(file, "wb")
        saveFile.write(bytearray(self.data))
        saveFile.close()

    def getData(self) -> list:
        return self.data
    
    def setData(self, index: int, value: int):
        self.data[index] = value
        self.refreshWigetsData()

    def refreshWigetsData(self):
        self.hexwidget.refreshData()
        self.textarea.refreshData()

    def notifyCursorPosToText(self):
        row, col = self.hexwidget.getCursorCoordinates()
        self.textarea.setCursorCoordinates(row, col)
    
    def notifyCursorPosToHex(self):
        row, col = self.textarea.getCursorCoordinates()
        self.hexwidget.setCursorCoordinates(row, col)

    def notifyScrollPosToText(self):
        self.textarea.verticalScrollBar().setValue(self.hexwidget.verticalScrollBar().value())

    def notifyScrollPosToHex(self):
        self.hexwidget.verticalScrollBar().setValue(self.textarea.verticalScrollBar().value())