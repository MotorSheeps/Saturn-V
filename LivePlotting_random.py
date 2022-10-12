import serial
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication)
from PyQt5 import QtWidgets, QtCore
import PyQt5
import time
import sys
import os
import pyqtgraph as pg
import numpy as np
from random import randint

class tempPlot(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        
        self.x = list(range(-101,-1))
        self.y = [randint(0,0) for _ in range(100)]

        self.setLabel("left", "Temperature (°C)")
        self.setLabel("bottom", "Second (S)")

        self.tempLine = self.plot(self.x, self.y, pen='g')
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):

        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]
        self.y.append(randint(0,100))
        
        self.tempLine.setData(self.x, self.y)


class presPlot(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        
        self.x = list(range(-101,-1))
        self.y = [randint(0,0) for _ in range(100)]

        self.setLabel("left", "Pressure (psi)")
        self.setLabel("bottom", "Second (S)")

        self.presLine = self.plot(self.x, self.y, pen='g')
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    def update_plot_data(self):

        presPen = pg.mkPen(color=(255,0,255))

        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]
        self.y.append(randint(0,100))
        
        self.presLine.setData(self.x, self.y)


class altiPlot(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        
        self.x = list(range(-101,-1))
        self.y = [randint(0,0) for _ in range(100)]

        self.setLabel("left", "Altitude (m)")
        self.setLabel("bottom", "Second (S)")

        self.altiLine = self.plot(self.x, self.y, pen='g')
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    def update_plot_data(self):

        altiPen = pg.mkPen(color=(255,0,255))

        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]
        self.y.append(randint(0,100))
        
        self.altiLine.setData(self.x, self.y)

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI() # call the UI set up

    # set up the UI
    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.pgtemp = tempPlot()
        self.pgpres = presPlot()
        self.pgalti = altiPlot()
        self.layout.addWidget(self.pgtemp)
        self.layout.addWidget(self.pgpres)
        self.layout.addWidget(self.pgalti)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

