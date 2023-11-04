from typing import Optional
from PySide6.QtCore import *
import PySide6.QtCore
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

import math

import re
import PySide6.QtWidgets
from overrides import override

from EditWidget import EditWidget
from OffsetArea import OffsetArea
from ByteIndexArea import ByteIndexArea

# Remove everything that's not hexadecimal
# text = re.sub("[^A-F,0-9]", "", text)

class Hexwidget(EditWidget):
    def __init__(self, data: bytes):
        super().__init__(data, 48, 3)
        
        # Custom Property
        self.editProgress = False

        # Widget Settings
        self.marginSize = QSize(40, 20)

        # Child Widgets
        self.lineNumberArea = OffsetArea(self)
        self.byteIndexArea = ByteIndexArea(self)

        # Event Connections
        self.blockCountChanged.connect(self.updateLineNumberWidth)
        self.verticalScrollBar().valueChanged.connect(self.lineNumberArea.scrollHandler)

        # Final Setup
        self.updateLineNumberWidth()
        self.refreshWidgets()

    @override
    def applyInput(self, input, index):
        if self.editProgress:
            self.data[index] = (self.data[index] & 0xF0) | (input & 0x0F)
            self.editProgress = False
        else:
            self.data[index] = (input << 4) | (self.data[index] & 0xF)
            self.editProgress = True

    @override
    def itemRight(self):
        self.editProgress = False
        return super().itemRight()
    
    @override
    def itemLeft(self):
        self.editProgress = False
        return super().itemLeft()
    
    @override
    def translateData(self, data: list):
        text = ""

        for b in data:
            text += f"{b:02X} "

        return text
    
    @override
    def translateInput(self, key: str):
        if (key.isnumeric()):
            return int(key)
        else:
            return None

    # Maybe merge up
    @override
    def cursorPosChanged(self):
        linePos = self.textCursor().positionInBlock()
        if (linePos % self.itemSize) == (self.itemSize - 1):
            self.itemRight()
            self.updateCursor()

        return super().cursorPosChanged()

    @override
    def highlightText(self):
        lineSelection = QTextEdit.ExtraSelection()
        lineSelection.format.setBackground(Qt.gray)
        lineSelection.cursor = self.textCursor()
        lineSelection.format.setProperty(QTextFormat.FullWidthSelection, True)

        byteSelection = QTextEdit.ExtraSelection()
        byteSelection.format.setBackground(Qt.yellow)
        byteSelection.format.setForeground(Qt.red)
        byteSelection.cursor = self.textCursor()
        byteSelection.cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)
        byteSelection.cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)

        self.setExtraSelections([lineSelection, byteSelection])

    def updateLineNumberWidth(self):
        # Set the margins Size
        self.setViewportMargins(self.marginSize.width(), self.marginSize.height(), 0, 0)

    def refreshWidgets(self):
        self.lineNumberArea.update()

    #@override
    #def getCursorPos(self):
    #    row = self.textCursor().blockNumber()
    #    col = math.floor(self.textCursor().positionInBlock() / 3)

    #    return row * self.lineLen + col
    
    #@override
    #def setCursorPos(self, row, col):
    #    pos = (row * 16 + col) * 3
    #    cursor = self.textCursor()
    #    cursor.setPosition(pos, QTextCursor.MoveAnchor)
    #    self.setTextCursor(cursor)