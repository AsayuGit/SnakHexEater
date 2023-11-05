from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from PIL import Image
from PIL import ExifTags
import io

class ImageDataWidget(QWidget):
    def __init__(self, imageData: bytes):
        super().__init__()

        layout = QVBoxLayout()

        self.exifTable = QTableWidget()
        self.exifTable.setColumnCount(2)
        self.exifTable.setHorizontalHeaderLabels(["Field", "Value"])
        self.exifTable.setColumnWidth(0, 150)
        self.exifTable.setColumnWidth(1, 300)
        
        layout.addWidget(self.exifTable)

        self.setLayout(layout)

        exif = self.loadExif(imageData)
        self.setExif(exif)

    def loadExif(self, data: bytes) -> dict:
        image = Image.open(io.BytesIO(data))

        exif = {
            ExifTags.TAGS[key]: value
            for key, value in image.getexif().items()
            if key in ExifTags.TAGS
        }

        return exif

    def setExif(self, exif: dict):
        for key, value in exif.items():
            keyCell = QTableWidgetItem(key)
            valueCell = QTableWidgetItem(str(value))

            self.exifTable.insertRow(self.exifTable.rowCount())
            self.exifTable.setItem(self.exifTable.rowCount() - 1, 0, keyCell)
            self.exifTable.setItem(self.exifTable.rowCount() - 1, 1, valueCell)