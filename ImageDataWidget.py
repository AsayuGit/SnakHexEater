from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from PIL import Image
from PIL import ExifTags
import io
import json

# When loaded attemps to parse and display a image's exif data
class ImageDataWidget(QWidget):
    def __init__(self, imageData: bytes):
        super().__init__()

        layout = QVBoxLayout()

        # Menu Bar
        self.exifMenuBar = QMenuBar()
        self.exifSaveMenu = self.exifMenuBar.addMenu("&Save")
                
        # Menu Actions
        self.exifSaveAction = QAction("&Save as json", self)
        self.exifSaveAction.setToolTip("Save exif data to disk")
        self.exifSaveAction.triggered.connect(self.doSaveExifJsonAction)

        self.exifSaveMenu.addAction(self.exifSaveAction)

        # Dialogs
        self.saveExifJsonDialog = QFileDialog(self)
        self.saveExifJsonDialog.setFileMode(QFileDialog.AnyFile)
        self.saveExifJsonDialog.setWindowTitle("Save Exif As...")
        self.saveExifJsonDialog.setAcceptMode(QFileDialog.AcceptSave)
        self.saveExifJsonDialog.fileSelected.connect(self.saveExifJson)

        # Exif Table
        self.exifTable = QTableWidget()
        self.exifTable.setColumnCount(2)
        self.exifTable.setHorizontalHeaderLabels(["Field", "Value"])
        self.exifTable.setColumnWidth(0, 150)
        self.exifTable.setColumnWidth(1, 300)

        # Layout Setup
        layout.addWidget(self.exifMenuBar)
        layout.addWidget(self.exifTable)

        # Final Setup
        self.setLayout(layout)

        exif = self.loadExif(imageData)
        if exif == {}:
            raise ValueError
        self.setExif(exif)

        self.exifData = exif

    # Loads the exif data from an image
    def loadExif(self, data: bytes) -> dict:
        image = Image.open(io.BytesIO(data))

        exif = {
            ExifTags.TAGS[key]: str(value)
            for key, value in image.getexif().items()
            if key in ExifTags.TAGS
        }

        return exif

    # Apply an exif dictionary to the exifTable
    def setExif(self, exif: dict):
        for key, value in exif.items():
            keyCell = QTableWidgetItem(key)
            valueCell = QTableWidgetItem(str(value))

            self.exifTable.insertRow(self.exifTable.rowCount())
            self.exifTable.setItem(self.exifTable.rowCount() - 1, 0, keyCell)
            self.exifTable.setItem(self.exifTable.rowCount() - 1, 1, valueCell)

    # Save the exif data to disk
    def doSaveExifJsonAction(self):
        self.saveExifJsonDialog.open()

    def saveExifJson(self, path: str):
        with open(path, "w") as file:
            json.dump(self.exifData, file, indent=4)