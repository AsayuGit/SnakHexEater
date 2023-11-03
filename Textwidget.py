from PySide6.QtCore import *
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

class Textwidget(QPlainTextEdit):
    def __init__(self, data: bytes):
        super().__init__()

        # Use a Fixed size font
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))
        self.setViewportMargins(0, 20, 0, 0)
        
        self.textChanged.connect(self.formatText)
        self.cursorPositionChanged.connect(self.highlightCurrentChar)

        self.setPlainText(data.decode("ascii").replace("\n", ".").replace("\t", "."))

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