import os
import sys

from PyQt5 import QtGui, QtWidgets, uic

from utils import img_converter as conv
from utils import gray_scale as gs
from utils import histogram as histo
from utils.blur import blur, gauss, median 

class Application(QtWidgets.QMainWindow):
    def __init__(self,uiPath):
        super().__init__()
        uic.loadUi(uiPath, self)
	
        self.img = None
        self.filename = None
        self.mode = None
        self.imgFormat = "rgb"
        self.convImg = []
        self.lastPath = os.getcwd()

        self.findChild(QtWidgets.QPushButton, ('openBut')).clicked.connect(self._openClicked)
        self.findChild(QtWidgets.QPushButton, ('convertBut')).clicked.connect(self._convert)
        self.findChild(QtWidgets.QPushButton, ('saveBut')).clicked.connect(self._saveConverted)
        
        self.listWidget = self.findChild(QtWidgets.QListWidget, ('listWidget'))
        
        self.previewLabel = self.findChild(QtWidgets.QLabel, ('previewLabel'))
        self.showLabel = self.findChild(QtWidgets.QLabel, ('showLabel'))
        self.consoleLabel = self.findChild(QtWidgets.QLabel, ('consoleLabel'))

        self.previewLabel.setHidden(True)
        self.showLabel.setHidden(True)
        
        #self.show()
        self.showMaximized()

    def _openClicked(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 
                'Open',self.lastPath,
                "Gambar (*.jpg *.jpeg *.png *.tif *.raw *.bmp *.JPG *.JPEG *.PNG *.TIF *.RAW *.BMP)")[0]
        splitPath = filename.split('/')
        self.lastPath = ""
        for x in splitPath[:-1]:
            self.lastPath = os.path.join(self.lastPath, x)
        if len(filename):
            self.filename = filename
            self.img, self.mode= conv.openImage(self.filename)
            self._showPhoto(self.img)
        self._print()

    def _convert(self):
        if not self.mode: 
            self._print("Gambar belum dipilih!")
            return
        
        choosen = self.listWidget.currentItem().text()
        if choosen == "Gray Scale":
            if self.mode == "L":
                self._print("Gambar sudah dalam bentuk grayscale")
                return
            else:
                self._print("Processing...")
                self.convImg = gs.grayScale(self.img, fromCV2 = True)
                self.imgFormat = "g"
        elif choosen == "Monochrome":
            self._print("Processing...")
            self.convImg = gs.monoChrome(self.img, fromCV2 = True)
            self.imgFormat = "g"
        elif choosen == "Average Blur":
            self._print("Processing...")
            self.convImg = blur(self.img)
            self.imgFormat = "rgb"
        elif choosen == "Gaussian Blur":
            self._print("Processing...")
            self.convImg = gauss(self.img)
            self.imgFormat = "rgb"
        elif choosen == "Median Blur":
            self._print("Processing...")
            self.convImg = median(self.img)
            self.imgFormat = "rgb"
        elif choosen == "CDF":
            self._print("Processing...")
            self.convImg = histo.equalize(self.img)
            self.imgFormat = "g"
            print(histo.hist(self.img,False))
        else:
            self._print("Mode belum dipilih!")
            return
        self._showPhoto(self.convImg, result = True)
        self._print("Done!")

    def _saveConverted(self):
        if len(self.convImg) > 0 :
            path = conv.saveImage(self.filename, self.convImg)
            self._print("Saved to %s" %path)
            return
        self._print("Nothing to save")

    def _bestFit(self, img, size):
        hScale = size/img.shape[0]
        wScale = size/img.shape[1]
        return hScale if hScale < wScale else wScale 

    def _showPhoto(self, image, result = False):
        #if not result:
        image = conv.rgbgr(image) if self.imgFormat == "rgb" else image

        image = conv.resize(image, scale = self._bestFit(image,480))
        image = QtGui.QImage(image,
                             image.shape[1],
                             image.shape[0],
                             image.strides[0],
                             QtGui.QImage.Format_RGB888 if self.imgFormat == "rgb" else QtGui.QImage.Format_Grayscale8)

        if result:
            #image = conv.rgbgr(image) if self.imgFormat == "rgb" else image
            self.showLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.showLabel.setHidden(False)
        else:
            self.previewLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.previewLabel.setHidden(False)
        self._print()

    def _print(self, text = ""):
        self.consoleLabel.setText("Console: %s"%text)

app = QtWidgets.QApplication(sys.argv)
def begin():
    window = Application("rootwindow.ui")
    sys.exit(app.exec_())

__all__ = ['app','Application','begin']

if __name__ == "__main__":
    begin()
