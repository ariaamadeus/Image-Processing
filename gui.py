import os
import sys

from PyQt5 import QtGui, QtWidgets, uic, QtCore
#from PySide2 import *

from utils import img_converter as conv
from utils.gray_scale import grayScale as gray
from utils.threshold import monoChrome, truncate, toZero, toZeroInv, otsu
from utils import histogram as histo
from utils import filters
from utils.blur import blur, gauss, median
from utils.contours import connected, contours, \
    conArea, perimeter, center, erode, dilate, opening, closing, gradient 

from graph.graph import linePlot

class Application(QtWidgets.QMainWindow):
    def __init__(self,uiPath):
        super().__init__()
        self.ui = uic.loadUi(uiPath, self) # uiPath = rootwindow.ui
	
        ''' Variabel'''
        
        self.img = []
        self.lastImg = []
        self.firstImg = []
        self.filename = None
        self.mode = None
        self.imgFormat = "rgb"
        self.convImg = []
        self.lastPath = os.getcwd()
        self.threshold = 127
        self.comboIndex = 0
        
        ''' Tombol '''
        
        self.findChild(QtWidgets.QAction, ('actionOpen_Image')).triggered.connect(self._openClicked) 
        self.findChild(QtWidgets.QAction, ('actionSave')).triggered.connect(self._saveConverted)
        self.findChild(QtWidgets.QAction, ('actionSave_2')).triggered.connect(self._saveConvertedLeft)
        self.findChild(QtWidgets.QAction, ('actionReset')).triggered.connect(self._resetImage)
        self.findChild(QtWidgets.QPushButton, ('geserBut')).clicked.connect(self._geser)
        convertBut = self.findChild(QtWidgets.QPushButton, ('convertBut'))
        
        convertBut.setVisible(False)

        ''' Stacked Widgets (depend ke pilihan dari Combo Box)'''

        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, ('stackedWidget'))

        ''' Combo Box '''
        
        self.comboBox = self.findChild(QtWidgets.QComboBox, ('comboBox'))
        
        self.comboBox.currentIndexChanged.connect(self._changeComboBox)
        
        ''' List Widgets (nempel ke Stacked Widgets) '''
        
        self.listWidget = self.findChild(QtWidgets.QListWidget, ('listWidget'))
        self.listWidget_2 = self.findChild(QtWidgets.QListWidget, ('listWidget_2'))
        self.listWidget_3 = self.findChild(QtWidgets.QListWidget, ('listWidget_3'))
        self.listWidget_4 = self.findChild(QtWidgets.QListWidget, ('listWidget_4'))
        self.listWidget_5 = self.findChild(QtWidgets.QListWidget, ('listWidget_5'))

        self.listWidget.itemClicked.connect(self._convert)
        self.listWidget_2.itemClicked.connect(self._convert)
        self.listWidget_3.itemClicked.connect(self._convert)
        self.listWidget_4.itemClicked.connect(self._convert)
        self.listWidget_5.itemClicked.connect(self._convert)
        
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
        
        ''' Dock Widgets '''

        self.dockWidget = self.findChild(QtWidgets.QDockWidget, ('dockWidget'))
        #self.dockWidget.setVisible(True)

        ''' Plot '''

        self.scrollArea = self.findChild(QtWidgets.QScrollArea, ('scrollArea'))
        self.linePlot = linePlot(title = "Histogram")
        self._createLinePlot(self.scrollArea, 0, self.linePlot)
        self.dockWidget.setVisible(False)

        ''' Drag & drop gambar '''
        
        # Kenapa tidak bisa yaa? :)
        #self.previewLabel.setAcceptDrops(True)
        #self.setAcceptDrops(True)

        ''' Show '''

        self.show()
        #self.showMaximized()

    def dropEvent(self,event):
        # Belum bisa
        if event.mimeData().hasImage():
            print('Ok')
            self._showPhoto(event.mimeData().imageData())
            #self.previewLabel.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))
    
    def _resetImage(self):
        self.img = self.firstImg
        self._showPhoto(self.img)

    def _createLinePlot(self, scrollArea, rowN, thePlot):
        frame = QtWidgets.QFrame(scrollArea)
        frame.setObjectName(u"frame")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
            QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
        frame.setSizePolicy(sizePolicy)
        frame.setMinimumSize(QtCore.QSize(800, 400))
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        gridLayout = QtWidgets.QGridLayout(frame)
        gridLayout.setObjectName(u"gridLayout")

        gridLayout.addWidget(thePlot.theGraph(),rowN,0,1,1)
        self.ui.gridLayout_9.addWidget(frame)

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
            self.firstImg = self.img
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
        
        # boolean
        histoBool = False

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
            if self.comboIndex == 5:
                choosen = self.listWidget_5.currentItem().text()
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
            # Plot Histogram
            maxHist = 0
            self.linePlot.clear()
            for i, rgbHist in enumerate(histo.hist(self.img, gs = False)):
                for j, hist in enumerate(rgbHist):
                    if hist > maxHist : maxHist = hist
                    self.linePlot.plotRGB(j, hist, color = i)
            self.linePlot.setYMax(maxHist+5)
            histoBool = True
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
        elif choosen == "Monochrome Inverse":
            self._print("Proses...")
            self.convImg = monoChrome(self.img, fromCV2 = True, threshold = self.threshold, invert = True)
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
        elif choosen == "Connected":
            self._print("Proses...")
            n, self.convImg = connected(self.img)
            print("%s Object"%n)
            self.imgFormat = "rgb"
        elif choosen == "Contours Mask":
            self._print("Proses...")
            self.convImg = contours(self.img, drawImg = self.img, draw = True, color = (0,255,255), thick = 4)
            self.imgFormat = "rgb"
        elif choosen == "Contours First Image":
            self._print("Proses...")
            self.convImg = contours(self.img, drawImg = self.firstImg, draw = True, color = (0,255,255), thick = 4)
            self.imgFormat = "rgb"
        elif choosen == "Erode":
            self._print("Proses...")
            self.convImg = erode(self.img, kernel = (5,5), itterations = 1)
            self.imgFormat = "rgb"
        elif choosen == "Dilate":
            self._print("Proses...")
            self.convImg = dilate(self.img, kernel = (5,5), itterations = 1)
            self.imgFormat = "rgb"
        elif choosen == "Opening":
            self._print("Proses...")
            self.convImg = opening(self.img, kernel = (5,5), itterations = 1)
            self.imgFormat = "rgb"
        elif choosen == "Closing":
            self._print("Proses...")
            self.convImg = closing(self.img, kernel = (5,5), itterations = 1)
            self.imgFormat = "rgb"
        elif choosen == "Gradient":
            self._print("Proses...")
            self.convImg = gradient(self.img, kernel = (5,5), itterations = 1)
            self.imgFormat = "rgb"
        elif choosen == "Glomerulus":
            self._print("Proses...")
            self.convImg = glomerulus(self.img)
            self.imgFormat = "rgb"
        else:
            self._print("Mode belum dipilih!")
            return -2

        self.dockWidget.setVisible(True) if histoBool else self.dockWidget.setVisible(False)

        self._showPhoto(self.convImg, result = True)
        self._print("Selesai!")
        return 0

    def _geser(self):
        #-1 Tidak ada gambar
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
        #-1 Tidak ada gambar
        if len(self.convImg) > 0 :
            path = conv.saveImage(self.filename, self.convImg)
            self._print("Kanan Tersimpan ke %s" %path)
            return 0
        self._print("Tidak ada gambar yang dapat disimpan")
        return -1

    def _saveConvertedLeft(self):
        if len(self.img) > 0 :
            path = conv.saveImage(self.filename, self.img)
            self._print("Kiri Tersimpan ke %s" %path)
            return 0
        self._print("Tidak ada gambar yang dapat disimpan")
        return -1

    def _bestFit(self, img, size):
        hScale = size/img.shape[0]
        wScale = size/img.shape[1]
        return hScale if hScale < wScale else wScale 

    def _showPhoto(self, image, result = False):
        if self._cekGambar() < 0 : return -1
        image = conv.rgbgr(image) if self.imgFormat == "rgb" else image

        image = conv.resize(image, scale = self._bestFit(image,480))
        image = QtGui.QImage(image,
                             image.shape[1],
                             image.shape[0],
                             image.strides[0],
                             QtGui.QImage.Format_RGB888 if self.imgFormat == "rgb" else QtGui.QImage.Format_Grayscale8)

        #image = image.transformed(QtGui.QTransform().rotate(50))
        if result:
            self.showLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.showLabel.setHidden(False)
        else:
            self.previewLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.previewLabel.setHidden(False)
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
