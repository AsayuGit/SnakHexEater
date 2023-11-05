from Hexeditor import Hexeditor

from overrides import override

class FileHexEditor(Hexeditor):
    def __init__(self, path: str):
        super().__init__()

        self.filePath = path

        file = open(path, "rb")
        self.setEditorData(file.read())
        file.close()

    @override
    def saveData(self):
        saveFile = open(self.filePath, "wb")
        saveFile.write(bytearray(self.data))
        saveFile.close()