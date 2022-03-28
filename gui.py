import sys

from PyQt5 import QtGui, QtWidgets, uic

from utils import img_converter as conv
from utils import gray_scale as gs

class Application(QtWidgets.QMainWindow):
    def __init__(self,uiPath):
        super().__init__()
        uic.loadUi(uiPath, self)

        self.img = None
        self.filename = None
        self.mode = None
        
        self.findChild(QtWidgets.QPushButton, ('openBut')).clicked.connect(self._openClicked)
        self.findChild(QtWidgets.QPushButton, ('convertBut')).clicked.connect(self._convert)
        self.findChild(QtWidgets.QPushButton, ('saveBut')).clicked.connect(self._saveConverted)
        
        self.listWidget = self.findChild(QtWidgets.QListWidget, ('listWidget'))
        
        self.previewLabel = self.findChild(QtWidgets.QLabel, ('previewLabel'))
        self.showLabel = self.findChild(QtWidgets.QLabel, ('showLabel'))
        
        self.previewLabel.setHidden(True)
        self.showLabel.setHidden(True)
        
        #self.show()
        self.showMaximized()

    def _openClicked(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open')[0]
        if len(filename):
            self.filename = filename
            self.img, self.mode= conv.openImage(self.filename)
            self._showPhoto(self.img)

    def _convert(self):
        if not self.mode:
            print("Gambar belum dipilih!")
            return
        choosen = self.listWidget.currentItem().text()
        if choosen == "Gray Scale":
            if self.mode == "L":
                print("Gambar sudah dalam bentuk grayscale")
            else:
                self.grayImg = gs.grayScale(self.img, fromCV2 = True)
                self._showPhoto(self.grayImg, result = True)

    def _saveConverted(self):
        conv.saveImage(self.filename, self.grayImg)

    def _showPhoto(self, image, result = False):
        if not result:
            image = conv.rgbgr(image)
        image = conv.resize(image, scale = 0.2)
        image = QtGui.QImage(image,
                             image.shape[1],
                             image.shape[0],
                             image.strides[0],
                             QtGui.QImage.Format_Grayscale8 if result else QtGui.QImage.Format_RGB888)

        if result:
            self.showLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.showLabel.setHidden(False)
        else:
            self.previewLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.previewLabel.setHidden(False)

app = QtWidgets.QApplication(sys.argv)
def begin():
    window = Application("rootwindow.ui")
    sys.exit(app.exec_())

__all__ = ['app','Application','begin']

if __name__ == "__main__":
    begin()
