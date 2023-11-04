import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from Hexeditor import Hexeditor

import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Application Settings
        self.setMinimumSize(1280, 600)

        # Widgets
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Menu Bar
        self.menuBar = QMenuBar()
        self.fileMenu = self.menuBar.addMenu("&File")

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)

        # Dialogs
        self.openFileDialog = QFileDialog(self)
        self.openFileDialog.setFileMode(QFileDialog.ExistingFile)
        self.openFileDialog.setWindowTitle("Open File...")
        self.openFileDialog.fileSelected.connect(self.doFilePicked)

        # Menu Bar Actions
        self.openAction = QAction("&Open File", self)
        self.openAction.setToolTip("Open a file from disk")
        self.openAction.triggered.connect(self.doOpenFileAction)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.setToolTip("Exit the program")
        self.exitAction.triggered.connect(self.doExitAction)

        # Tabs actions
        self.tabs.tabCloseRequested.connect(self.doCloseTab)
        
        # Assign menu bar actions
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.exitAction)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.menuBar)
        layout.addWidget(self.tabs)

        central_widget.setLayout(layout)

    def doOpenFileAction(self):
        self.openFileDialog.open()

    def doFilePicked(self, file: str):
        self.tabs.addTab(Hexeditor(file), os.path.basename(file))

    def doCloseTab(self, id: int):
        self.tabs.removeTab(id)

    def doExitAction(self):
        exit(0)

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("Hexeditor")
window.show()
app.exec()
