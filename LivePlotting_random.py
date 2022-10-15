#Graph libraries
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication)
from PyQt5 import QtWidgets, QtCore, QtGui
import PyQt5
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Normal libraries
import serial
import time
import sys
import os
from random import randint

#---------------------------------------------------------------
#  Plotting Code Starts Here
#---------------------------------------------------------------

xi = 2
maxRange = 60
packetInterval = 100 #time in milliseconds between updates

class tempPlot(pg.PlotWidget):
    def __init__(tempGraph):
        pg.PlotWidget.__init__(tempGraph)
        
        tempGraph.x = list(range(-(xi),0))
        tempGraph.y = [randint(0,0) for _ in range(xi)]
        tempGraph.storeY = [tempGraph.y[-1] for _ in range(xi)]
        tempGraph.avg = [0 for _ in range(len(tempGraph.x))]
        tempGraph.storeAvg = [0 for _ in range(len(tempGraph.x))]

        tempGraph.setLabel('left', 'Temperature (°C)')
        tempGraph.setLabel('bottom', 'Second (s)')
        tempGraph.setTitle('Temperature')

        tempGraph.tempAvg = tempGraph.plot(tempGraph.x, tempGraph.storeAvg, pen='b')
        tempGraph.tempLine = tempGraph.plot(tempGraph.x, tempGraph.y, pen='k')
        tempGraph.setBackground('w')
        tempGraph.showGrid(x=True, y=True)
        
        tempGraph.timer = QtCore.QTimer()
        tempGraph.timer.setInterval(packetInterval)
        tempGraph.timer.timeout.connect(tempGraph.update_plot_data)
        tempGraph.timer.start()

    def update_plot_data(tempGraph):

        xi = len(tempGraph.x)

        if xi < maxRange:
            
            tempGraph.x.append(tempGraph.x[-1] + 1)
            tempGraph.y.append(randint(0,100))
            tempGraph.storeY.append(tempGraph.y[-1])

        else:
            
            tempGraph.x = tempGraph.x[1:]
            tempGraph.x.append(tempGraph.x[-1] + 1)

            tempGraph.y = tempGraph.y[1:]
            tempGraph.y.append(randint(0,100))
            tempGraph.storeY.append(tempGraph.y[-1])

        if len(tempGraph.x) > 12:
            if xi >= maxRange:
                tempGraph.avg = tempGraph.avg[1:]
                
            tempGraph.avg.append(sum(tempGraph.storeY[11:]) / len(tempGraph.storeY[11:]))
            tempGraph.tempAvg.setData(tempGraph.x, tempGraph.avg)
                
        else:

            tempGraph.avg.append(1)

        tempGraph.tempLine.setData(tempGraph.x, tempGraph.y)
      
        xiRead = QtWidgets.QLineEdit(str(xi))


class presPlot(pg.PlotWidget):
    def __init__(presGraph):
        pg.PlotWidget.__init__(presGraph)
        
        presGraph.x = list(range(-(xi),0))
        presGraph.y = [randint(0,0) for _ in range(xi)]
        presGraph.storeY = [presGraph.y[-1] for _ in range(xi)]
        presGraph.avg = [0 for _ in range(len(presGraph.x))]
        presGraph.storeAvg = [0 for _ in range(len(presGraph.x))]

        presGraph.setLabel('left', 'Pressure (torr)')
        presGraph.setLabel('bottom', 'Second (s)')
        presGraph.setTitle('Pressure')

        presGraph.presAvg = presGraph.plot(presGraph.x, presGraph.storeAvg, pen='b')
        presGraph.presLine = presGraph.plot(presGraph.x, presGraph.y, pen='k')
        presGraph.setBackground('w')
        presGraph.showGrid(x=True, y=True)
        
        presGraph.timer = QtCore.QTimer()
        presGraph.timer.setInterval(packetInterval)
        presGraph.timer.timeout.connect(presGraph.update_plot_data)
        presGraph.timer.start()
        
    def update_plot_data(presGraph):

        xi = len(presGraph.x)

        if xi < maxRange:
            
            presGraph.x.append(presGraph.x[-1] + 1)
            presGraph.y.append(randint(700,840))
            presGraph.storeY.append(presGraph.y[-1])

        else:
            
            presGraph.x = presGraph.x[1:]
            presGraph.x.append(presGraph.x[-1] + 1)

            presGraph.y = presGraph.y[1:]
            presGraph.y.append(randint(700,840))
            presGraph.storeY.append(presGraph.y[-1])

            

        if len(presGraph.x) > 12:
            if xi >= maxRange:
                presGraph.avg = presGraph.avg[1:]

            presGraph.avg.append(sum(presGraph.storeY[11:]) / len(presGraph.storeY[11:]))
            presGraph.presAvg.setData(presGraph.x, presGraph.avg)
                
        else:

            presGraph.avg.append(1)

        presGraph.presLine.setData(presGraph.x, presGraph.y)


class altiPlot(pg.PlotWidget):
    def __init__(altiGraph):
        pg.PlotWidget.__init__(altiGraph)
        
        altiGraph.x = list(range(-(xi),0))
        altiGraph.y = [randint(0,0) for _ in range(xi)]

        altiGraph.setLabel('left', 'Altitude (m)')
        altiGraph.setLabel('bottom', 'Second (s)')
        altiGraph.setTitle('Altitude')

        altiGraph.altiLine = altiGraph.plot(altiGraph.x, altiGraph.y, pen='k')
        altiGraph.setBackground('w')
        altiGraph.showGrid(x=True, y=True)
        altiGraph.setYRange(0, 600, padding=0)
        
        altiGraph.timer = QtCore.QTimer()
        altiGraph.timer.setInterval(packetInterval)
        altiGraph.timer.timeout.connect(altiGraph.update_plot_data)
        altiGraph.timer.start()
        
    def update_plot_data(altiGraph):

        xi = len(altiGraph.x)

        altiGraph.x.append(altiGraph.x[-1] + 1)
        altiGraph.y.append(pow((altiGraph.x[-1] / 15), 2))
        
        altiGraph.altiLine.setData(altiGraph.x, altiGraph.y)


class Window(QWidget):

    def __init__(wind):
        super().__init__()

        wind.initUI() # call the UI set up

    def manualRelease(wind):
            print('AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')

    # set up the UI
    def initUI(wind):
        
        layout = QtWidgets.QGridLayout()
        wind.setLayout(layout)
        wind.layout = QVBoxLayout(wind)
        wind.setGeometry(0,0,1920,1080)
        
        wind.pgtemp = tempPlot()
        wind.pgpres = presPlot()
        wind.pgalti = altiPlot()

        layout.addWidget(wind.pgtemp, 0, 0, 2, 2)
        layout.addWidget(wind.pgpres, 0, 2, 2, 2)
        layout.addWidget(wind.pgalti, 2, 0, 2, 2)

        font = 30
        MRB = QtWidgets.QPushButton('⚠\nEJECT\n⚠', wind)
        MRB.setToolTip('WARNING: EMERGENCY ONLY')
        MRB.resize(5*font,5*font)
        MRB.move(999, 569)
        MRB.setStyleSheet('background-color : red')
        MRB.setFont(QFont('Arial', font))
        MRB.clicked.connect(wind.manualRelease)

        wind.show()
        wind.setWindowTitle('LivePlotting_L')
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('antialias',True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

