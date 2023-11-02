from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from Hexwidget import Hexwidget

class Hexeditor(QWidget):
    def __init__(self, path: str):
        super().__init__()

        layout = QHBoxLayout()

        self.hexwidget = Hexwidget()
        self.textarea = QPlainTextEdit()

        layout.addWidget(self.hexwidget)
        layout.addWidget(self.textarea)

        self.setLayout(layout)

        self.loadFile(path)

    def loadFile(self, path: str):
        file = open(path, "rb")
        text = file.read()

        print(text)