import os
import sys

from PyQt5 import QtGui, QtWidgets, uic

from utils import img_converter as conv
from utils.gray_scale import grayScale as gray
from utils.threshold import monoChrome, truncate, toZero, toZeroInv, otsu
from utils import histogram as histo
from utils import filters
from utils.blur import blur, gauss, median

class Application(QtWidgets.QMainWindow):
    def __init__(self,uiPath):
        super().__init__()
        uic.loadUi(uiPath, self) # uiPath = rootwindow.ui
	
        ''' Variabel'''
        
        self.img = None
        self.lastImg = None
        self.filename = None
        self.mode = None
        self.imgFormat = "rgb"
        self.convImg = []
        self.lastPath = os.getcwd()
        self.threshold = 127
        self.comboIndex = 0
        
        ''' Tombol '''
        
        #self.findChild(QtWidgets.QPushButton, ('openBut')).clicked.connect(self._openClicked)
        #self.findChild(QtWidgets.QPushButton, ('saveBut')).clicked.connect(self._saveConverted)
        self.findChild(QtWidgets.QAction, ('actionOpen_Image')).triggered.connect(self._openClicked) 
        self.findChild(QtWidgets.QAction, ('actionSave')).triggered.connect(self._saveConverted)
        #self.findChild(QtWidgets.QPushButton, ('convertBut')).clicked.connect(self._convert)
        convertBut = self.findChild(QtWidgets.QPushButton, ('convertBut'))
        self.findChild(QtWidgets.QPushButton, ('geserBut')).clicked.connect(self._geser)
        
        convertBut.setVisible(False)
        ''' Stacked Widgets (depend ke pilihan dari Combo Box)'''

        #self.stackedWidget = self.findChild(QtGui.QStackedWidget, ('stackedWidget'))
        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, ('stackedWidget'))

        ''' Combo Box '''
        
        self.comboBox = self.findChild(QtWidgets.QComboBox, ('comboBox'))
        
        self.comboBox.currentIndexChanged.connect(self._changeComboBox)
        
        ''' List Widgets (nempel ke Stacked Widgets) '''
        
        self.listWidget = self.findChild(QtWidgets.QListWidget, ('listWidget'))
        self.listWidget_2 = self.findChild(QtWidgets.QListWidget, ('listWidget_2'))
        self.listWidget_3 = self.findChild(QtWidgets.QListWidget, ('listWidget_3'))
        self.listWidget_4 = self.findChild(QtWidgets.QListWidget, ('listWidget_4'))

        self.listWidget.itemClicked.connect(self._convert)
        self.listWidget_2.itemClicked.connect(self._convert)
        self.listWidget_3.itemClicked.connect(self._convert)
        self.listWidget_4.itemClicked.connect(self._convert)
        
        ''' Spin Box '''

        self.spinBox_4 = self.findChild(QtWidgets.QSpinBox, ('spinBox_4'))

        self.spinBox_4.valueChanged.connect(self._convertSpin)

        ''' Label '''
        
        self.previewLabel = self.findChild(QtWidgets.QLabel, ('previewLabel'))
        self.showLabel = self.findChild(QtWidgets.QLabel, ('showLabel'))
        self.showLClone = self.showLabel
        self.consoleLabel = self.findChild(QtWidgets.QLabel, ('consoleLabel'))

        self.previewLabel.setHidden(True)
        self.showLabel.setHidden(True)
        
        ''' Drag & drop gambar '''
        
        #self.previewLabel.setAcceptDrops(True)
        #self.setAcceptDrops(True)

        ''' show '''

        self.show()
        #self.showMaximized()

    def _changeComboBox(self, val):
        self.comboIndex = val
        self.stackedWidget.setCurrentIndex(val)
        if val == 0:
            self._convert()

    def _openClicked(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 
                'Buka',self.lastPath,
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

    def _cekGambar(self, geser = False):
        #-1:belum ada gambar , -2:gambar belum dikonversi
        try:
            if not self.img: 
                self._print("Gambar belum dipilih!")
                return -1
        except:
            try:
                if not self.convImg and geser:
                    self._print("Gambar belum dikonversi!")
                    return -2
            except:
                pass
        return 0

    def _convertSpin(self):
        self.threshold = self.spinBox_4.value()
        self._convert()

    def _convert(self):
        #-1 sudah dikonversi, -2: gambar belum dipilih
        if self._cekGambar() < 0 : return -1
        
        # Cek list terpilih
        try:
            if self.comboIndex == 0:
                choosen = "Gray Scale"
            if self.comboIndex == 1:
                choosen = self.listWidget.currentItem().text()
            if self.comboIndex == 2:
                choosen = self.listWidget_2.currentItem().text()
            if self.comboIndex == 3:
                choosen = self.listWidget_3.currentItem().text()
            if self.comboIndex == 4:
                choosen = self.listWidget_4.currentItem().text()
        except:
            choosen = ''
        if choosen == "Gray Scale":
            if self.mode == 'L' or self.mode == '1':
                self._print("Gambar sudah dalam bentuk Gray Scale")
                return -1
            else:
                self._print("Proses...")
                self.convImg = gray(self.img, fromCV2 = True)
                self.imgFormat = "g"
        elif choosen == "Average Blur":
            self._print("Proses...")
            self.convImg = blur(self.img)
            self.imgFormat = "rgb"
        elif choosen == "Gaussian Blur":
            self._print("Proses...")
            self.convImg = gauss(self.img)
            self.imgFormat = "rgb"
        elif choosen == "Median Blur":
            self._print("Proses...")
            self.convImg = median(self.img)
            self.imgFormat = "rgb"
        elif choosen == "CDF":
            self._print("Proses...")
            self.convImg = histo.equalize(self.img)
            self.imgFormat = "g"
            print(histo.hist(self.img,False))
        elif choosen == "CLAHE":
            self._print("Proses...")
            self.convImg = histo.clahe(self.img)
            self.imgFormat = "g"
        elif choosen == "Bilateral":
            self._print("Proses...")
            self.convImg = filters.bilateral(self.img)
            self.imgFormat = "rgb"
        elif choosen == "Sobel":
            self._print("Proses...")
            self.convImg = filters.sobel(self.img)
            self.imgFormat = "g"
        elif choosen == "Monochrome":
            self._print("Proses...")
            self.convImg = monoChrome(self.img, fromCV2 = True, threshold = self.threshold)
            self.imgFormat = "g"
        elif choosen == "Truncate":
            self._print("Proses...")
            self.convImg = truncate(self.img, threshold = self.threshold)
            self.imgFormat = "g"
        elif choosen == "To Zero":
            self._print("Proses...")
            self.convImg = toZero(self.img, threshold = self.threshold)
            self.imgFormat = "g"
        elif choosen == "To Zero Inverted":
            self._print("Proses...")
            self.convImg = toZeroInv(self.img, threshold = self.threshold)
            self.imgFormat = "g"
        elif choosen == "Otsu":
            self._print("Proses...")
            self.convImg = otsu(self.img, threshold = self.threshold)
            self.imgFormat = "g"
        else:
            self._print("Mode belum dipilih!")
            return -2

        self._showPhoto(self.convImg, result = True)
        self._print("Selesai!")
        return 0

    def _geser(self):
        if self._cekGambar(geser = True) < 0 : return -1
        
        try:
            self.lastImg = self.img
            self.img = self.convImg
            self._showPhoto(self.img, False)
            self.showLabel = self.showLClone
        
            self.mode = conv.modeCheck(self.img)
        except:
            return -1
        return 0

    def _saveConverted(self):
        if len(self.convImg) > 0 :
            path = conv.saveImage(self.filename, self.convImg)
            self._print("Tersimpan ke %s" %path)
            return 0
        self._print("Tidak ada gambar yang dapat disimpan")
        return -1

    def _bestFit(self, img, size):
        hScale = size/img.shape[0]
        wScale = size/img.shape[1]
        return hScale if hScale < wScale else wScale 

    def _showPhoto(self, image, result = False):
        image = conv.rgbgr(image) if self.imgFormat == "rgb" else image

        image = conv.resize(image, scale = self._bestFit(image,480))
        image = QtGui.QImage(image,
                             image.shape[1],
                             image.shape[0],
                             image.strides[0],
                             QtGui.QImage.Format_RGB888 if self.imgFormat == "rgb" else QtGui.QImage.Format_Grayscale8)

        if result:
            self.showLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.showLabel.setHidden(False)
        else:
            self.previewLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.previewLabel.setHidden(False)
            if self.comboIndex == 0:
                self._convert()
        self._print()

    def _print(self, text = ""):
        #print ke console GUI
        self.consoleLabel.setText("Console: %s"%text)

app = QtWidgets.QApplication(sys.argv)
def begin():
    window = Application("rootwindow.ui")
    sys.exit(app.exec_())

__all__ = ['app','Application','begin']

if __name__ == "__main__":
    begin()
