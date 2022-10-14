#XBee
import digi.xbee

#Graph libraries
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication)
from PyQt5 import QtWidgets, QtCore
import PyQt5
import pyqtgraph as pg

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
maxRange = 100
packetInterval = 100 #time in milliseconds between updates

class tempPlot(pg.PlotWidget):
    def __init__(tempGraph):
        pg.PlotWidget.__init__(tempGraph)
        
        tempGraph.x = list(range(-(xi),0))
        tempGraph.y = [randint(0,0) for _ in range(xi)]
        tempGraph.avg = sum(tempGraph.y) / len(tempGraph.x)
        tempGraph.storeAvg = [tempGraph.avg for _ in range(len(tempGraph.x))]

        tempGraph.setLabel('left', 'Temperature (°C)')
        tempGraph.setLabel('bottom', 'Second (s)')
        tempGraph.setTitle('Temperature')

        tempGraph.tempAvg = tempGraph.plot(tempGraph.x, tempGraph.storeAvg, pen='b')
        tempGraph.tempLine = tempGraph.plot(tempGraph.x, tempGraph.y, pen='g')
        tempGraph.showGrid(x=True, y=True)
        
        tempGraph.timer = QtCore.QTimer()
        tempGraph.timer.setInterval(packetInterval)
        tempGraph.timer.timeout.connect(tempGraph.update_plot_data)
        tempGraph.timer.start()

    def update_plot_data(tempGraph):

        xi = len(tempGraph.x)

        tempGraph.avg = sum(tempGraph.y) / len(tempGraph.x)

        if xi < maxRange:
            
            tempGraph.x.append(tempGraph.x[-1] + 1)
            tempGraph.y.append(randint(0,100))
            tempGraph.storeAvg.append(tempGraph.avg)

        else:
            
            tempGraph.x = tempGraph.x[1:]
            tempGraph.x.append(tempGraph.x[-1] + 1)

            tempGraph.y = tempGraph.y[1:]
            tempGraph.y.append(randint(0,100))

            tempGraph.storeAvg = tempGraph.storeAvg[1:]
            tempGraph.storeAvg.append(tempGraph.avg)

        tempGraph.tempAvg.setData(tempGraph.x, tempGraph.storeAvg)
        tempGraph.tempLine.setData(tempGraph.x, tempGraph.y)
      
        xiRead = QtWidgets.QLineEdit(str(xi))


class presPlot(pg.PlotWidget):
    def __init__(presGraph):
        pg.PlotWidget.__init__(presGraph)
        
        presGraph.x = list(range(-(xi),0))
        presGraph.y = [randint(0,0) for _ in range(xi)]
        presGraph.avg = sum(presGraph.y) / len(presGraph.x)
        presGraph.storeAvg = [presGraph.avg for _ in range(len(presGraph.x))]

        presGraph.setLabel('left', 'Pressure (hPa)')
        presGraph.setLabel('bottom', 'Second (s)')
        presGraph.setTitle('Pressure')

        presGraph.presAvg = presGraph.plot(presGraph.x, presGraph.storeAvg, pen='b')
        presGraph.presLine = presGraph.plot(presGraph.x, presGraph.y, pen='g')
        presGraph.showGrid(x=True, y=True)
        
        presGraph.timer = QtCore.QTimer()
        presGraph.timer.setInterval(packetInterval)
        presGraph.timer.timeout.connect(presGraph.update_plot_data)
        presGraph.timer.start()
        
    def update_plot_data(presGraph):

        xi = len(presGraph.x)

        presGraph.avg = sum(presGraph.y) / len(presGraph.x)

        if xi < maxRange:
            
            presGraph.x.append(presGraph.x[-1] + 1)
            presGraph.y.append(randint(0,100))
            presGraph.storeAvg.append(presGraph.avg)

        else:
            
            presGraph.x = presGraph.x[1:]
            presGraph.x.append(presGraph.x[-1] + 1)

            presGraph.y = presGraph.y[1:]
            presGraph.y.append(randint(0,100))

            presGraph.storeAvg = presGraph.storeAvg[1:]
            presGraph.storeAvg.append(presGraph.avg)

        presGraph.presAvg.setData(presGraph.x, presGraph.storeAvg)
        presGraph.presLine.setData(presGraph.x, presGraph.y)


class altiPlot(pg.PlotWidget):
    def __init__(altiGraph):
        pg.PlotWidget.__init__(altiGraph)
        
        altiGraph.x = list(range(-100,0))
        altiGraph.y = [randint(0,0) for _ in range(100)]

        altiGraph.setLabel('left', 'Altitude (m)')
        altiGraph.setLabel('bottom', 'Second (s)')
        altiGraph.setTitle('Altitude')

        altiGraph.altiLine = altiGraph.plot(altiGraph.x, altiGraph.y, pen='g')
        altiGraph.showGrid(x=True, y=True)
        
        altiGraph.timer = QtCore.QTimer()
        altiGraph.timer.setInterval(packetInterval)
        altiGraph.timer.timeout.connect(altiGraph.update_plot_data)
        altiGraph.timer.start()
        
    def update_plot_data(altiGraph):

        altiGraph.x = altiGraph.x[1:]
        altiGraph.x.append(altiGraph.x[-1] + 1)

        altiGraph.y = altiGraph.y[1:]
        altiGraph.y.append(randint(0,100))
        
        altiGraph.altiLine.setData(altiGraph.x, altiGraph.y)

class Window(QWidget):

    def __init__(wind):
        super().__init__()

        wind.initUI() # call the UI set up

    # set up the UI
    def initUI(wind):
        layout = QtWidgets.QGridLayout()
        wind.setLayout(layout)
        wind.layout = QVBoxLayout(wind)

        
        wind.pgtemp = tempPlot()
        wind.pgpres = presPlot()
        wind.pgalti = altiPlot()

        
        layout.addWidget(wind.pgtemp, 0, 0, 2, 2)
        layout.addWidget(wind.pgpres, 0, 2, 2, 2)
        layout.addWidget(wind.pgalti, 2, 0, 2, 2)

        wind.show()
        wind.setWindowTitle('LivePlotting_L')
        pg.setConfigOption('background', 'k')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

