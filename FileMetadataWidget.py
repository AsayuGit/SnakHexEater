from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

import os
import time
import math

class FileMetadataWidget(QWidget):
    def __init__(self, path: str):
        super().__init__()

        # Layout setup
        layout = QVBoxLayout()

        # Widgets
        self.metadataTable = QTableWidget()
        self.metadataTable.setColumnCount(2)
        self.metadataTable.setHorizontalHeaderLabels(["Metadata", "Value"])
        self.metadataTable.setColumnWidth(0, 150)
        self.metadataTable.setColumnWidth(1, 300)

        layout.addWidget(self.metadataTable)

        self.setLayout(layout)

        # Loads metadata from the file
        self.loadMetadata(path)

    def loadMetadata(self, path: str):
        filestats = os.stat(path)

        self.metadataTable.setRowCount(0)

        # Assotiate each metadata to its name
        data = {
            "Created": time.ctime(os.path.getctime(path)),
            "Last Modified": time.ctime(os.path.getmtime(path)),
            "Size": self.byteToHuman(filestats.st_size),
            "Inode": filestats.st_ino,
            "UID": filestats.st_uid,
            "GID": filestats.st_gid,
            "Mode": filestats.st_mode,
            "Device ID": filestats.st_dev,
        }

        # Then add each value to the metadata table
        for key, value in data.items():
            keyCell = QTableWidgetItem(key)
            valueCell = QTableWidgetItem(str(value))

            self.metadataTable.insertRow(self.metadataTable.rowCount())
            self.metadataTable.setItem(self.metadataTable.rowCount() - 1, 0, keyCell)
            self.metadataTable.setItem(self.metadataTable.rowCount() - 1, 1, valueCell)

    # Convert a filesize in Byte to a human readable from up to a Tebibyte
    def byteToHuman(self, size: int) -> str:
        if size < 0x400:
            return f"{size} B"
        elif size < 0x100000:
            return f"{math.floor(size / 0x400)} KiB" # Kibibyte
        elif size < 0x40000000:
            return f"{math.floor(size / 0x100000)} MiB" # Mebibyte
        elif size < 0x1000000000:
            return f"{math.floor(size / 0x40000000)} GiB" # Gibibyte
        else:
            return f"{math.floor(size / 0x1000000000)} TiB" # Tebibyte