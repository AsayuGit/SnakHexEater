from PySide6.QtCore import *
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import re

class Textwidget(QPlainTextEdit):
    def __init__(self, data: bytes):
        super().__init__()

        # Use a Fixed size font
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.setViewportMargins(0, 20, 0, 0)
        self.setTextInteractionFlags(Qt.TextEditable)
        
        self.textChanged.connect(self.formatText)
        self.cursorPositionChanged.connect(self.highlightCurrentChar)

        text = re.sub(r'[^0-9a-zA-Z]+', '.', data.decode("ascii", errors="replace"))
        self.setPlainText(text)

    def formatText(self):
        self.blockSignals(True)

        text = self.toPlainText()
        text = "\n".join(text[i:i+16] for i in range(0, len(text), 16))
        self.setPlainText(text)

        self.blockSignals(False)

    def highlightCurrentChar(self):
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

    def setCursorPos(self, row, col):
        if col >= 16:
            col = 15

        cursor = self.textCursor()
        cursor.setPosition(row * 17 + col, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def getCursorPos(self) -> (int, int):
        row = self.textCursor().blockNumber()
        col = self.textCursor().positionInBlock()

        return (row, col)