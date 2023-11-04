from PySide6.QtCore import *
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import re

from overrides import override

from EditWidget import EditWidget

class Textwidget(EditWidget):
    def __init__(self, data: bytes):
        super().__init__(data, 16)

    @override
    def translateData(self, data: list) -> str:
        text = ""

        for b in data:
            c = chr(b)
            if b < 0x21 or b > 0x7E:
                c = '.'
            text += c

        return text

    @override
    def highlightText(self):
        lineSelection = QTextEdit.ExtraSelection()
        lineSelection.format.setBackground(Qt.gray)
        lineSelection.cursor = self.textCursor()
        lineSelection.format.setProperty(QTextFormat.FullWidthSelection, True)

        charSelection = QTextEdit.ExtraSelection()
        charSelection.format.setBackground(Qt.yellow)
        charSelection.format.setForeground(Qt.red)
        charSelection.cursor = self.textCursor()
        charSelection.cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor)
        charSelection.cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)

        self.setExtraSelections([lineSelection, charSelection])