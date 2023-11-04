from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from Hexwidget import Hexwidget
from Textwidget import Textwidget

class Hexeditor(QWidget):
    def __init__(self, path: str):
        super().__init__()
        
        # Widget Settings
        layout = QHBoxLayout()

        # Initial Setup
        file = open(path, "rb")
        self.data = [b for b in file.read()]

        # Child Widgets
        self.hexwidget = Hexwidget(self)
        self.textarea = Textwidget(self)

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
        layout.addWidget(self.hexwidget)
        layout.addWidget(self.textarea)
        self.setLayout(layout)

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