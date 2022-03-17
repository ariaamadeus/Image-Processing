import sys

from PyQt5 import QtGui, QtWidgets, uic

from utils import imgConverter as conv

class Application(QtWidgets.QMainWindow):
    def __init__(self,uiPath):
        super().__init__()
        uic.loadUi(uiPath, self)

        self.img = None
        self.filename = ''

        self.findChild(QtWidgets.QPushButton, ('openBut')).clicked.connect(self._openClicked)
        self.findChild(QtWidgets.QPushButton, ('convertBut')).clicked.connect(self._convert)
        self.findChild(QtWidgets.QPushButton, ('saveBut')).clicked.connect(self._saveConverted)
        self.previewLabel = self.findChild(QtWidgets.QLabel, ('previewLabel'))
        self.showLabel = self.findChild(QtWidgets.QLabel, ('showLabel'))
        self.show()

    def _openClicked(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open')[0]
        if len(filename):
            self.filename = filename
            self.img, self.mode= conv.openImage(self.filename)
            self._showPhoto(self.img)

    def _convert(self):
        if self.mode == "L":
            print("Gambar sudah dalam bentuk grayscale")
        else:
            self.grayImg = conv.grayScale(self.img)
            self._showPhoto(self.grayImg, result = True)

    def _saveConverted(self):
        conv.saveImage(self.filename, self.grayImg)

    def _showPhoto(self, image, result = False):
        self.tmp = image
        if not result:
            image = conv.rgbgr(image)
        image = conv.resize(image, scale = 0.5)
        image = QtGui.QImage(image,
                             image.shape[1],
                             image.shape[0],
                             image.strides[0],
                             QtGui.QImage.Format_Indexed8 if result else QtGui.QImage.Format_RGB888)

        if result:
            self.showLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        else:
            self.previewLabel.setPixmap(QtGui.QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Application("mainwindow.ui")
    sys.exit(app.exec_())
