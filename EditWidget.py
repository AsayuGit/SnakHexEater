from PySide6.QtCore import *
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
import re

from overrides import override
from abc import abstractclassmethod

import math

class EditWidget(QPlainTextEdit):
    def __init__(self, data: bytes, lineLen: int, itemSize: int):
        super().__init__()

        # Put the data in a data array
        self.data = [b for b in data]
        self.lineLen = lineLen
        self.itemSize = itemSize
        
        # Custom properties
        self.dataIndex = 0

        self.cursorRow = 0
        self.cursorCol = 0

        # Widget settings
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont)) # Use a Fixed size font
        self.setViewportMargins(0, 20, 0, 0)
        self.setTextInteractionFlags(Qt.TextEditable)
        
        # Envent Connections
        self.cursorPositionChanged.connect(self.cursorPosChanged)

        self.updateText()

    @abstractclassmethod
    def highlightText(self): pass

    @abstractclassmethod
    def translateData(self, data: list): pass

    @abstractclassmethod
    def translateInput(self, key: str): pass

    # At each keypress, put the corresponding ascii char in the data array
    # An move the cursor pos
    @override
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Up:
            self.cursorUp()
            self.updateCursor()
        elif e.key() == Qt.Key.Key_Down:
            self.cursorDown()
            self.updateCursor()
        elif e.key() == Qt.Key.Key_Left:
            self.cursorLeft()
            self.updateCursor()
        elif e.key() == Qt.Key.Key_Right:
            self.cursorRight()
            self.updateCursor()
        else:
            self.data[self.getCursorPos()] = self.translateInput(e.text())
            self.cursorRight()
            self.updateText()

    def cursorRight(self):
        # Ensure we're at the start of the next item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize) + self.itemSize

        if self.cursorCol >= self.lineLen:
            self.cursorCol = 0
            self.cursorRow += 1
    
    def cursorLeft(self):
        if self.cursorRow > 0 and self.cursorCol <= 0:
            self.cursorCol = self.lineLen - 1
            self.cursorRow -= 1
        elif self.cursorCol > 0:
            self.cursorCol -= self.itemSize

        # Ensure we're at the start of the previous item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize)

    def cursorUp(self):
        if self.cursorRow > 0:
            self.cursorRow -= 1

    def cursorDown(self):
        self.cursorRow += 1

    def getCursorPos(self):
        return self.cursorRow * self.lineLen + self.cursorCol
    
    def setCursorPos(self, row, col):
        pass

    def toEndOfLine(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def cursorPosChanged(self):
        linePos = self.textCursor().positionInBlock()
        if linePos >= self.lineLen:
            self.toEndOfLine()

        self.cursorRow = self.textCursor().blockNumber()
        self.cursorCol = self.textCursor().positionInBlock()

        self.highlightText()

    def updateCursor(self):
        cursor = self.textCursor()
        #  + to take in account the \n in the widget text
        cursor.setPosition(self.getCursorPos() + self.cursorRow, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def updateText(self):
        text = self.translateData(self.data)
        text = self.formatText(text)
        
        self.blockSignals(True)
        self.setPlainText(text)
        self.blockSignals(False)

        self.updateCursor()
        self.highlightText()

    def formatText(self, text):
        return "\n".join(text[i:i + self.lineLen] for i in range(0, len(text), self.lineLen))