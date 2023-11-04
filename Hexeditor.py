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
        text = file.read()

        # Child Widgets
        self.hexwidget = Hexwidget(text)
        self.textarea = Textwidget(text)
        self.scrollbar = QScrollBar()

        # Widgets Settings
        self.textarea.setCursorPos(0, 0)
        self.hexwidget.setCursorPos(0, 0)

        #self.hexwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.hexwidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Event Connections
        #self.hexwidget.cursorPositionChanged.connect(self.notifyCursorPosToText)
        #self.textarea.cursorPositionChanged.connect(self.notifyCursorPosToHex)
        self.scrollbar.valueChanged.connect(self.scrollWidgets)
        self.scrollbar.rangeChanged.connect(self.range)
        #self.hexwidget.verticalScrollBar().valueChanged.connect(self.notifyScrollPosToText)
        #self.textarea.verticalScrollBar().valueChanged.connect(self.notifyScrollPosToHex)

        # Final Setup
        # Ensure the scrollbar is of the right size
        self.range()
        
        # Layout Setup
        layout.addWidget(self.hexwidget)
        layout.addWidget(self.textarea)
        layout.addWidget(self.scrollbar)
        self.setLayout(layout)

    def notifyCursorPosToText(self):
        # row, col = self.hexwidget.getCursorPos()
        # self.textarea.setCursorPos(row, col)
        pass
    
    def notifyCursorPosToHex(self):
        pass
        #row, col = self.textarea.getCursorPos()
        #self.hexwidget.setCursorPos(row, col)

    def notifyScrollPosToText(self):
        # self.scrollbar.setValue(self.hexwidget.verticalScrollBar().value())
        pass

    def notifyScrollPosToHex(self):
        #self.scrollbar.setValue(self.textarea.verticalScrollBar().value())
        pass

    def scrollWidgets(self):
        pass
        #self.hexwidget.verticalScrollBar().setSliderPosition(self.scrollbar.value())
        #self.textarea.verticalScrollBar().setSliderPosition(self.scrollbar.value())

    def range(self):
        #max = self.hexwidget.verticalScrollBar().maximum()
        #min = self.hexwidget.verticalScrollBar().minimum()

        #self.scrollbar.setMaximum(max)
        #self.scrollbar.setMinimum(min)
        pass