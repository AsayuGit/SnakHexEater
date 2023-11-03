from typing import Optional
from PySide6.QtCore import *
import PySide6.QtCore
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

import re
import PySide6.QtWidgets
from overrides import override

class Hexwidget(QPlainTextEdit):
    def __init__(self, data: bytes):
        super().__init__()
        
        self.marginSize = QSize(40, 20)

        # Use a Fixed size font
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        
        # Can write over existing characters
        self.setOverwriteMode(True)
        self.setCurrentCharFormat(QTextCharFormat(QTextFormat()))

        # Connect the signal trigered when the text changes
        self.textChanged.connect(self.formatText)

        self.lineNumberArea = OffsetArea(self)

        self.blockCountChanged.connect(self.updateLineNumberWidth)
        self.updateLineNumberWidth()

        self.cursorPositionChanged.connect(self.highlightCurrentOctet)

        self.byteIndexArea = ByteIndexArea(self)

        self.setPlainText(data.hex())
    
    def formatText(self):        
        # Block Signals to avoid recursion
        self.blockSignals(True)
        
        # Ensure the input text is in uppercase
        text = self.toPlainText().upper()
        # Remove everything that's not hexadecimal
        text = re.sub("[^A-F,0-9]", "", text)
        # Group text by 2
        text = " ".join(text[i:i+2] for i in range(0, len(text), 2))

        # Wrap test every 16 octet
        text = "\n".join(text[i:i+48].strip() for i in range(0, len(text), 48))

        # Set the modified text as new content
        self.setPlainText(text)

        self.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)

        # Set the cursor back at the end of the line with its enchor to continue editing and without sellecting

        # Turn back the signals on after operation
        self.blockSignals(False)

        self.refreshWidgets()

    def updateLineNumberWidth(self):
        # Set the margins Size
        self.setViewportMargins(self.marginSize.width(), self.marginSize.height(), 0, 0)
    
    def highlightCurrentOctet(self):
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

        '''
        self.blockSignals(True)
        self.moveCursor(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)
        self.blockSignals(False)
        '''

    def refreshWidgets(self):
        self.lineNumberArea.update()


class OffsetArea(QWidget): 
    def __init__(self, parent: Hexwidget):
        super().__init__(parent)
        self.hexwidget = parent
        self.move(0, self.hexwidget.marginSize.height())

    # The widget recommanded size
    @override
    def sizeHint(self) -> QSize:
        return QSize(self.hexwidget.marginSize.width(), self.hexwidget.height() - self.hexwidget.marginSize.height())

    @override
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)
        painter.setPen(Qt.black)

        block = self.hexwidget.firstVisibleBlock()

        # for each line
        while block.isValid():
            blockNumber = block.blockNumber()

            # Figure out line boundaries
            top = round(self.hexwidget.blockBoundingGeometry(block).translated(self.hexwidget.contentOffset()).top()) + 1
            bottom = top + round(self.hexwidget.blockBoundingRect(block).height())

            # Draw the line offset
            painter.drawText(0, top, self.hexwidget.marginSize.width(), self.fontMetrics().height(), Qt.AlignRight, f"{blockNumber * 16:#04x}")

            # get next line
            block = block.next()

class ByteIndexArea(QWidget):
    def __init__(self, parent: Hexwidget):
        super().__init__(parent)
        self.hexwidget = parent
        self.move(self.hexwidget.marginSize.width(), 0)

    @override
    def sizeHint(self) -> QSize:
        return QSize(self.hexwidget.height() - self.hexwidget.marginSize.width(), self.hexwidget.marginSize.height())
    
    @override
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)
        painter.setPen(Qt.black)
        
        painter.drawText(5, self.height() - self.fontMetrics().height(), self.width(), self.fontMetrics().height(), Qt.AlignLeft, (" ".join(f"{i:02x}" for i in range(0, 16))))