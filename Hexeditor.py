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
        self.scrollbar = QScrollBar()

        self.hexwidget.cursorPositionChanged.connect(self.notifyCursorPosToText)
        self.textarea.cursorPositionChanged.connect(self.notifyCursorPosToHex)

        self.scrollbar.valueChanged.connect(self.scrollWidgets)

        layout.addWidget(self.hexwidget)
        layout.addWidget(self.textarea)
        layout.addWidget(self.scrollbar)

        self.textarea.setCursorPos(0)
        self.hexwidget.setCursorPos(0)

        self.hexwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hexwidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.textarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.hexwidget.verticalScrollBar().valueChanged.connect(self.notifyScrollPosToText)
        self.textarea.verticalScrollBar().valueChanged.connect(self.notifyScrollPosToHex)

        self.setLayout(layout)

    def notifyCursorPosToText(self):
        self.textarea.setCursorPos(self.hexwidget.textCursor().position() / 3)
    
    def notifyCursorPosToHex(self):
        self.hexwidget.setCursorPos(self.textarea.textCursor().position() * 3)

    def notifyScrollPosToText(self):
        self.scrollbar.setValue(self.hexwidget.verticalScrollBar().value())

    def notifyScrollPosToHex(self):
        self.scrollbar.setValue(self.textarea.verticalScrollBar().value())

    def scrollWidgets(self):
        self.hexwidget.verticalScrollBar().setSliderPosition(self.scrollbar.value())
        self.textarea.verticalScrollBar().setSliderPosition(self.scrollbar.value())