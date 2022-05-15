# try:
    # from PySide2 import QtGui, QtCore
    # from PySide2.QtCharts import QtCharts
    # from PySide2.QtGui import QPainter
    # from PySide2.QtWidgets import *
# except:
from PyQt5 import QtGui, QtCore
import PyQt5.QtChart as QtCharts
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *

import sys

from random import randint

import time

import numpy as np

class linePlot():
    def __init__(self, title):
        self.chart = QtCharts.QChart()
        self.lineSeries = QtCharts.QLineSeries()
        self.count = 0
        self.x_min, self.x_max = (0,255)
        self.y_min, self.y_max = (0,255)
        self.LS = []

        #self.chart.addSeries(self.lineSeries)
        self.chart.setTitle(title)

        self.axisX = QtCharts.QValueAxis()
        self.axisX.setMax(self.x_max)
        self.axisX.setMin(self.x_min)
        self.chart.addAxis(self.axisX, QtCore.Qt.AlignBottom)
        self.lineSeries.attachAxis(self.axisX)

        self.axisY = QtCharts.QValueAxis()
        self.axisY.setMax(self.y_max)
        self.axisY.setMin(self.y_min)
        self.chart.addAxis(self.axisY, QtCore.Qt.AlignLeft)
        self.lineSeries.attachAxis(self.axisY)
        #self.chart.createDefaultAxes()

        self.chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.lineSeries.setColor(QtGui.QColor("darkblue"))
        self.chart.setAnimationDuration(100)
        self.chartView.setChart(self.chart)
        self.chartView.setRubberBand(QtCharts.QChartView.HorizontalRubberBand)
        for x in range (0,3):
            self.createLine(x)

    def theGraph(self):
        return self.chartView
    
    def clear(self):
        for line in self.LS:
            line.clear()

    def setYMax(self,value):
        self.axisY.setMax(value)

    def createLine(self, color = 0):
        
        #RGB plot
        lineSeries = QtCharts.QLineSeries()
        if color == 0 :
            lineSeries.setColor(QtGui.QColor("darkblue"))
        elif color == 1 :
            lineSeries.setColor(QtGui.QColor("darkgreen"))
        elif color == 2 :
            lineSeries.setColor(QtGui.QColor("darkred"))
            self.count = 0

        self.chart.addSeries(lineSeries)
        lineSeries.attachAxis(self.axisX)
        lineSeries.attachAxis(self.axisY)
        self.LS.append(lineSeries)

    def plot(self, x, y):
        #moving plot
        if self.count >= self.x_max:
            self.chart.scroll(self.chart.plotArea().width()/(self.axisX.max()-self.axisX.min()),0)
            time.sleep(0.01)
        
        self.count+=1
        self.lineSeries.append(x, y)

        if self.count >= 500:
            self.lineSeries.removePoints(0,250)
            self.count = 250
            time.sleep(0.01)
    
    def plotRGB(self, x, y, color):
        lineSeries = self.LS[color]
        lineSeries.append(x, y)

class barPlot():
    def __init__(self, title):
        self.chart = QtCharts.QChart()
        self.barSet = QtCharts.QBarSet("Lux")
        self.barSeries = QtCharts.QBarSeries()
        self.count = 0
        self.x_max = 40
        self.y_max = 5

        self.chart.addSeries(self.barSeries)
        self.chart.setTitle(title)

        self.categories = ["esp-1", "esp-2"]
        for x in self.categories:
            self.barSet.append(2)
        self.barSeries.append(self.barSet)
        
        self.axisX = QtCharts.QBarCategoryAxis()
        self.axisX.append(self.categories)
        self.chart.setAxisX(self.axisX, self.barSeries)
        self.axisX.setRange("esp-1","esp-2")

        self.axisY = QtCharts.QValueAxis()
        self.axisY.setMax(self.y_max)
        self.axisY.setMin(0)
        self.chart.setAxisY(self.axisY, self.barSeries)
        #self.chart.createDefaultAxes()

        self.chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.chart.setAnimationDuration(100)
        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chartView.setChart(self.chart)
        self.chartView.setRubberBand(QtCharts.QChartView.HorizontalRubberBand)

    def theGraph(self):
        return self.chartView
    
    def clear(self):
        pass

    def plot(self, data):
        pass
        for i, x in enumerate(data):
            self.barSet.replace(i, x)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    plot = barPlot(title = "Bar")
    plot = linePlot(title = "Line")
    print('OKE')
    #sys.exit(app.exec_())
