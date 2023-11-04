from PySide6.QtCore import *
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import re

from overrides import override

class Textwidget(QPlainTextEdit):
    def __init__(self, data: bytes):
        super().__init__()

        # Put the data in a data array
        self.data = [b for b in data]
        
        # Custom properties
        self.cursorRow = 0
        self.cursorCol = 0

        # Widget settings
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont)) # Use a Fixed size font
        self.setViewportMargins(0, 20, 0, 0)
        self.setTextInteractionFlags(Qt.TextEditable)
        
        # Envent Connections
        self.cursorPositionChanged.connect(self.cursorPosChanged)

        self.updateText()

    # At each keypress, put the corresponding ascii char in the data array
    # An move the cursor pos
    @override
    def keyPressEvent(self, e: QKeyEvent) -> None:
        self.data[self.getCursorPos()] = ord(e.text())
        self.advenceCursor()
        self.updateText()

    def advenceCursor(self):
        self.cursorCol += 1

        if self.cursorCol >= 16:
            self.cursorCol = 0
            self.cursorRow += 1          

    def getCursorPos(self):
        return self.cursorRow * 16 + self.cursorCol

    def toEndOfLine(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def cursorPosChanged(self):
        linePos = self.textCursor().positionInBlock()
        if linePos >= 16:
            self.toEndOfLine()

        self.cursorRow = self.textCursor().blockNumber()
        self.cursorCol = self.textCursor().positionInBlock()

        self.highlightCurrentChar()

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

    def updateCursor(self):
        cursor = self.textCursor()
        #  + to take in account the \n in the widget text
        cursor.setPosition(self.getCursorPos() + self.cursorRow, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def updateText(self):
        text = self.toASCII(self.data)
        text = self.formatText(text)
        
        self.blockSignals(True)
        self.setPlainText(text)
        self.blockSignals(False)

        self.updateCursor()
        self.highlightCurrentChar()

    def toASCII(self, data: list) -> str:
        text = ""

        for b in data:
            c = chr(b)
            if b < 0x21 or b > 0x7E:
                c = '.'
            text += c

        return text

    def formatText(self, text):
        return "\n".join(text[i:i+16] for i in range(0, len(text), 16))

    def setCursorPos(self, row, col):
        if col >= 16:
            col = 15

        cursor = self.textCursor()
        cursor.setPosition(row * 17 + col, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)