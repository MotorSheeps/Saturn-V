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
            presGraph.y.append(randint(700,800))
            presGraph.storeY.append(presGraph.y[-1])

        else:
            
            presGraph.x = presGraph.x[1:]
            presGraph.x.append(presGraph.x[-1] + 1)

            presGraph.y = presGraph.y[1:]
            presGraph.y.append(randint(700,800))
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


class plot4(pg.PlotWidget):
    def __init__(plot4Graph):
        pg.PlotWidget.__init__(plot4Graph)
        
        plot4Graph.x = list(range(-(xi),0))
        plot4Graph.y = [randint(0,0) for _ in range(xi)]
        plot4Graph.storeY = [plot4Graph.y[-1] for _ in range(xi)]
        plot4Graph.avg = [0 for _ in range(len(plot4Graph.x))]
        plot4Graph.storeAvg = [0 for _ in range(len(plot4Graph.x))]

        plot4Graph.setLabel('left', 'details')
        plot4Graph.setLabel('bottom', 'Second (s)')
        plot4Graph.setTitle('plot4')

        plot4Graph.plot4Avg = plot4Graph.plot(plot4Graph.x, plot4Graph.storeAvg, pen='b')
        plot4Graph.plot4Line = plot4Graph.plot(plot4Graph.x, plot4Graph.y, pen='k')
        plot4Graph.setBackground('w')
        plot4Graph.showGrid(x=True, y=True)
        
        plot4Graph.timer = QtCore.QTimer()
        plot4Graph.timer.setInterval(packetInterval)
        plot4Graph.timer.timeout.connect(plot4Graph.update_plot_data)
        plot4Graph.timer.start()

    def update_plot_data(plot4Graph):

        xi = len(plot4Graph.x)

        if xi < maxRange:
            
            plot4Graph.x.append(plot4Graph.x[-1] + 1)
            plot4Graph.y.append(randint(0,100))
            plot4Graph.storeY.append(plot4Graph.y[-1])

        else:
            
            plot4Graph.x = plot4Graph.x[1:]
            plot4Graph.x.append(plot4Graph.x[-1] + 1)

            plot4Graph.y = plot4Graph.y[1:]
            plot4Graph.y.append(randint(0,100))
            plot4Graph.storeY.append(plot4Graph.y[-1])

        if len(plot4Graph.x) > 12:
            if xi >= maxRange:
                plot4Graph.avg = plot4Graph.avg[1:]
                
            plot4Graph.avg.append(sum(plot4Graph.storeY[11:]) / len(plot4Graph.storeY[11:]))
            plot4Graph.plot4Avg.setData(plot4Graph.x, plot4Graph.avg)
                
        else:

            plot4Graph.avg.append(1)

        plot4Graph.plot4Line.setData(plot4Graph.x, plot4Graph.y)
      
        xiRead = QtWidgets.QLineEdit(str(xi))


class MRB(QtWidgets.QPushButton):

    def manualRelease(MRB):
        print('AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
    
    def __init__(MRB):

        QtWidgets.QPushButton.__init__(MRB)

        MRB.setText('⚠\nEJECT\n⚠')
        MRB.setToolTip('WARNING: EMERGENCY ONLY')
        MRB.setStyleSheet('background-color : red')
        MRB.setFont(QFont('Arial', 25))
        MRB.setGeometry(10,10,175,175)
        MRB.clicked.connect(MRB.manualRelease)


class Window(QWidget):

    def __init__(wind):
        super().__init__()

        wind.initUI() # call the UI set up

    # set up the UI
    def initUI(wind):
        
        layout = QtWidgets.QGridLayout()
        wind.setLayout(layout)
        wind.layout = QVBoxLayout(wind)
        wind.setGeometry(0,0,1920,1080)
        
        wind.pgtemp = tempPlot()
        wind.pgpres = presPlot()
        wind.pgalti = altiPlot()
        wind.pgplot4 = plot4()
        wind.MRB = MRB()

        layout.addWidget(wind.pgtemp, 0, 0, 20, 20)
        layout.addWidget(wind.pgpres, 20, 0, 20, 20)
        layout.addWidget(wind.pgalti, 0, 20, 20, 15)
        layout.addWidget(wind.pgplot4, 40, 0, 20, 20)
        layout.addWidget(wind.MRB, 20, 20)

        wind.show()
        wind.setWindowTitle('LivePlotting_L')
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('antialias',True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

