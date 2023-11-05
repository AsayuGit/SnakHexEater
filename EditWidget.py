from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from overrides import override
from abc import abstractclassmethod

import math

class EditWidget(QPlainTextEdit):
    indexChanged = Signal(int, int)
    
    def __init__(self, dataStore, lineLen: int, itemSize: int):
        super().__init__()
        
        # The data backend
        self.dataStore = dataStore
        self.data = []
        
        # Data representation properties
        self.lineLen = lineLen
        self.itemSize = itemSize

        # Cursor position on its data
        self.cursorRow = 0
        self.cursorCol = 0

        # Widget settings
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont)) # Use a Fixed size font
        self.setViewportMargins(0, 20, 0, 0)
        self.setTextInteractionFlags(Qt.TextEditable)
        
        # Envent Connections
        self.cursorPositionChanged.connect(self.cursorPosChanged)

        self.refreshData()

    # Theses methods are implementation dependant and thus are abstract
    # This method highlight the octet the cursor is on
    @abstractclassmethod
    def highlightText(self): pass

    # This method convert the data to a format relevant to the implementation
    @abstractclassmethod
    def translateData(self, data: list): pass

    # This method convert the input data from the keyboard to a format relevant to the implementation
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
            self.itemLeft()
            self.updateCursor()
        elif e.key() == Qt.Key.Key_Right:
            self.itemRight()
            self.updateCursor()
        else:
            input = self.translateInput(e.text())
            if input is not None:
                self.applyInput(input, self.getDataPos())
                self.cursorRight()
                self.updateCursor()
                self.refreshData()

    def applyInput(self, input, index):
        self.dataStore.setData(index, input)

    # Move the cursor to the byte on its right
    def itemRight(self):
        oldCursorCol = self.cursorCol
        oldCursorRow = self.cursorRow
        
        # Ensure we're at the start of the next item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize) + self.itemSize

        if self.cursorCol >= self.lineLen:
            self.cursorCol = 0
            self.cursorRow += 1

        if self.getDataPos() > len(self.data) - 1:
            self.cursorCol = oldCursorCol
            self.cursorRow = oldCursorRow
        else: 
            self.indexChanged.emit(self.cursorCol, self.cursorRow)

    # Move the cursor to the byte on its left
    def itemLeft(self):
        if self.cursorRow > 0 and self.cursorCol <= 0:
            self.cursorCol = self.lineLen - 1
            self.cursorRow -= 1
        elif self.cursorCol > 0:
            self.cursorCol -= self.itemSize

        if self.cursorCol < 0:
            self.cursorCol = 0

        self.indexChanged.emit(self.cursorCol, self.cursorRow)

        # Ensure we're at the start of the previous item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize)

    # Move the cursor 1 char to the right
    def cursorRight(self):
        # Ensure we're at the start of the next item
        self.cursorCol += 1

        if self.cursorCol >= self.lineLen:
            self.cursorCol = 0
            self.cursorRow += 1
    
    # Move the cursor 1 char to the left
    def cursorLeft(self):
        if self.cursorRow > 0 and self.cursorCol <= 0:
            self.cursorCol = self.lineLen - 1
            self.cursorRow -= 1
        elif self.cursorCol > 0:
            self.cursorCol -= 1

        # Ensure we're at the start of the previous item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize)

    # Move the cursor one line up
    def cursorUp(self):
        if self.cursorRow > 0:
            self.cursorRow -= 1
            self.indexChanged.emit(self.cursorCol, self.cursorRow)

    # Move the cursor one line down
    def cursorDown(self):
        oldCursorRow = self.cursorRow
        self.cursorRow += 1

        if self.getDataPos() > len(self.data) - 1:
            self.cursorRow = oldCursorRow
        else: 
            self.indexChanged.emit(self.cursorCol, self.cursorRow)

    def getCursorPos(self):
        return self.cursorRow * self.lineLen + self.cursorCol
    
    def setCursorPos(self, pos):
        pass

    def getDataPos(self):
        return math.floor(self.getCursorPos() / self.itemSize)
    
    # Returns the cursor absolute coordinates relative to the data
    def getCursorCoordinates(self):
        return (self.cursorRow, math.floor(self.cursorCol / self.itemSize))
    
    # Set the cursor to absolute cooridnates relative to the data
    def setCursorCoordinates(self, row, col):
        self.cursorRow = row
        self.cursorCol = col * self.itemSize
        self.updateCursor()

    # Put the cursor at the start of the next line
    def toNextLine(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

        self.indexChanged.emit(self.cursorCol, self.cursorRow)

    # Event triggered when the cursor changes position
    def cursorPosChanged(self):
        linePos = self.textCursor().positionInBlock()
        if linePos >= self.lineLen:
            self.toNextLine()


        oldCursorRow = self.cursorRow
        oldCursorCol = self.cursorCol

        self.cursorRow = self.textCursor().blockNumber()
        self.cursorCol = self.textCursor().positionInBlock()

        # Only emit the indexChanged signal if we changed byte
        # Some fomat may take more than one char to display a byte
        if (oldCursorRow != self.cursorRow) or (math.floor(oldCursorCol / self.itemSize) != math.floor(self.cursorCol / self.itemSize)):
            self.indexChanged.emit(self.cursorCol, self.cursorRow)

        self.highlightText()

    # Apply the cursor position to the widget's text cursor
    def updateCursor(self):
        cursor = self.textCursor()
        #  + to take in account the \n in the widget text
        pos = self.getCursorPos() + self.cursorRow

        cursor.setPosition(pos, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    # Refresh the data of the widget
    def refreshData(self):
        self.data = self.dataStore.getData()
        text = self.translateData(self.data)
        text = self.formatText(text)
        
        self.blockSignals(True)
        self.setPlainText(text)
        self.blockSignals(False)

        self.updateCursor()
        self.highlightText()

    # This method format the text in lines of lineLen
    def formatText(self, text):
        return "\n".join(text[i:i + self.lineLen] for i in range(0, len(text), self.lineLen))