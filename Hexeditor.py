from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from Hexwidget import Hexwidget
from Textwidget import Textwidget

class Hexeditor(QWidget):
    def __init__(self, path: str):
        super().__init__()

        layout = QHBoxLayout()

        file = open(path, "rb")
        text = file.read()

        self.hexwidget = Hexwidget(text)
        self.textarea = Textwidget(text)

        self.hexwidget.cursorPositionChanged.connect(self.notifyCursorPosToText)
        self.textarea.cursorPositionChanged.connect(self.notifyCursorPosToHex)

        layout.addWidget(self.hexwidget)
        layout.addWidget(self.textarea)

        self.setLayout(layout)

    def notifyCursorPosToText(self):
        self.textarea.setCursorPos(self.hexwidget.textCursor().position() / 3)
    
    def notifyCursorPosToHex(self):
        self.hexwidget.setCursorPos(self.textarea.textCursor().position() * 3)