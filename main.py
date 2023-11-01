import sys
import time
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from Hexwidget import Hexwidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        layout.addWidget(Hexwidget())

        central_widget.setLayout(layout)

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("Hexeditor")
window.show()
app.exec()
