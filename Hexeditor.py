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

        layout.addWidget(self.hexwidget)
        layout.addWidget(self.textarea)

        self.setLayout(layout)