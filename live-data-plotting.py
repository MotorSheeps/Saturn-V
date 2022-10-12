# AAAAAA

import serial
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication)
from PyQt5 import QtWidgets
import PyQt5
import time
import sys
import os
import pyqtgraph as pg
import numpy as np

# i forgor how to python
# altitude shit
class altitude(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        # actual graph parameters below
        self.x = [1,2,3] # x axis will need to be time since t=0 launch, this is a placeholder data set
        self.y = [1,2,3] # y axis will need to be imported altitude value
        self.setTitle("Altitude")
        self.plot(self.x, self.y)

# another graph, temp or whatever
class temp(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        # same as before
        self.x = [1,2,3] # same x axis as altitude
        self.y = [3,1,2] # imported temp values
        self.setTitle("Temperature")
        self.plot(self.x, self.y)

# pressure
class pressure(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        # same as before
        self.x = [1,2,3] # same x axis as altitude
        self.y = [3,2,2] # imported temp values
        self.setTitle("Pressure")
        self.plot(self.x, self.y)

# top container to hold everything
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # set the ui up

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.pgaltitude = altitude()
        self.pgtemp = temp()
        self.pgpressure = pressure()

        self.layout.addWidget(self.pgaltitude)
        self.layout.addWidget(self.pgtemp)
        self.layout.addWidget(self.pgpressure)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
