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


xi = 2
maxRange = 60
packetInterval = 1000 #time in milliseconds between updates

'''Packet delivers as [1005,MISIION_TIME,PACKET_COUNT,SW_STATE,PL_STATE,ALTITUDE,TEMP,
VOLTAGE,GYRO_R,GYRO_P,GYRO_Y]'''

t = 1
p = 1
A = 500
T = randint(0,40)
V = randint(0,1)
R = randint(0,400)
P = randint(0,400)
Y = randint(0,400)
        
packet = [1005,t,p,'ACTIVE','DESCENT',A,T,V,R,P,Y]

#Manual Release Code
class MRB(QtWidgets.QPushButton): #MRB = manual release button

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


class packetUpdate():
    def updater():
        global packet, t, p, A, T, V, R, P, Y
        
        t = 1 + t
        p = 1 + p
        A = A - (t^2)/15
        T = randint(0,40)
        V = randint(0,1)
        R = randint(0,400)
        P = randint(0,400)
        Y = randint(0,400)
        packet = [1005,t,p,'ACTIVE','DESCENT',A,T,V,R,P,Y]

#---------------------------------------------------------------
#  Plotting Code Starts Here
#---------------------------------------------------------------

class plots(pg.PlotWidget):

    class tempGraph(pg.PlotWidget):
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
            
            packetUpdate.updater()
            
            if xi < maxRange:
                
                tempGraph.x.append(tempGraph.x[-1] + 1)
                tempGraph.y.append(packet[6])
                tempGraph.storeY.append(tempGraph.y[-1])

            else:
                
                tempGraph.x = tempGraph.x[1:]
                tempGraph.x.append(tempGraph.x[-1] + 1)

                tempGraph.y = tempGraph.y[1:]
                tempGraph.y.append(packet[6])
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


    class voltGraph(pg.PlotWidget):
        def __init__(voltGraph):
            pg.PlotWidget.__init__(voltGraph)
            
            voltGraph.x = list(range(-(xi),0))
            voltGraph.y = [randint(0,0) for _ in range(xi)]

            voltGraph.setLabel('left', 'Voltage (V)')
            voltGraph.setLabel('bottom', 'Second (s)')
            voltGraph.setTitle('Voltage')

            voltGraph.voltLine = voltGraph.plot(voltGraph.x, voltGraph.y, pen='k')
            voltGraph.setBackground('w')
            voltGraph.showGrid(x=True, y=True)
            
            voltGraph.timer = QtCore.QTimer()
            voltGraph.timer.setInterval(packetInterval)
            voltGraph.timer.timeout.connect(voltGraph.update_plot_data)
            voltGraph.timer.start()
            
        def update_plot_data(voltGraph):

            xi = len(voltGraph.x)

            packetUpdate.updater()

            if xi < maxRange:
                
                voltGraph.x.append(voltGraph.x[-1] + 1)
                voltGraph.y.append(packet[7])

            else:
                
                voltGraph.x = voltGraph.x[1:]
                voltGraph.x.append(voltGraph.x[-1] + 1)

                voltGraph.y = voltGraph.y[1:]
                voltGraph.y.append(packet[7])

            voltGraph.voltLine.setData(voltGraph.x, voltGraph.y)


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
            altiGraph.y.append(packet[5])
            
            altiGraph.altiLine.setData(altiGraph.x, altiGraph.y)


    class gyroPlot(pg.PlotWidget):
        def __init__(gyroPlotGraph):
            pg.PlotWidget.__init__(gyroPlotGraph)
            
            gyroPlotGraph.x = list(range(-(xi),0))
            gyroPlotGraph.yR = [randint(0,0) for _ in range(xi)]
            gyroPlotGraph.yP = [randint(0,0) for _ in range(xi)]
            gyroPlotGraph.yY = [randint(0,0) for _ in range(xi)]

            gyroPlotGraph.setLabel('left', 'details')
            gyroPlotGraph.setLabel('bottom', 'Second (s)')
            gyroPlotGraph.setTitle('Gyroscope')

            gyroPlotGraph.gyroPlotLineR = gyroPlotGraph.plot(gyroPlotGraph.x, gyroPlotGraph.yR, pen='r')
            gyroPlotGraph.gyroPlotLineP = gyroPlotGraph.plot(gyroPlotGraph.x, gyroPlotGraph.yP, pen='b')
            gyroPlotGraph.gyroPlotLineY = gyroPlotGraph.plot(gyroPlotGraph.x, gyroPlotGraph.yY, pen='k')
            gyroPlotGraph.setBackground('w')
            gyroPlotGraph.showGrid(x=True, y=True)
            
            gyroPlotGraph.timer = QtCore.QTimer()
            gyroPlotGraph.timer.setInterval(packetInterval)
            gyroPlotGraph.timer.timeout.connect(gyroPlotGraph.update_plot_data)
            gyroPlotGraph.timer.start()

        def update_plot_data(gyroPlotGraph):

            xi = len(gyroPlotGraph.x)

            packetUpdate.updater()

            if xi < maxRange:
                
                gyroPlotGraph.x.append(gyroPlotGraph.x[-1] + 1)
                gyroPlotGraph.yR.append(packet[8])
                gyroPlotGraph.yP.append(packet[9])
                gyroPlotGraph.yY.append(packet[10])

            else:
                
                gyroPlotGraph.x = gyroPlotGraph.x[1:]
                gyroPlotGraph.x.append(gyroPlotGraph.x[-1] + 1)

                gyroPlotGraph.yR = gyroPlotGraph.yR[1:]
                gyroPlotGraph.yP = gyroPlotGraph.yP[1:]
                gyroPlotGraph.yY = gyroPlotGraph.yY[1:]
                gyroPlotGraph.yR.append(packet[8])
                gyroPlotGraph.yP.append(packet[9])
                gyroPlotGraph.yY.append(packet[10])

            gyroPlotGraph.gyroPlotLineR.setData(gyroPlotGraph.x, gyroPlotGraph.yR)
            gyroPlotGraph.gyroPlotLineP.setData(gyroPlotGraph.x, gyroPlotGraph.yP)
            gyroPlotGraph.gyroPlotLineY.setData(gyroPlotGraph.x, gyroPlotGraph.yY)

#---------------------------------------------------------------
#  Plotting Code Endss Here
#---------------------------------------------------------------

class Window(QWidget):
    def __init__(wind):
        super().__init__()

        wind.initUI() # call the UI set up

    def initUI(wind):
        
        layout = QtWidgets.QGridLayout()
        wind.setLayout(layout)
        wind.layout = QVBoxLayout(wind)
        wind.setGeometry(0,0,1920,1080)
        
        wind.pgtemp = plots.tempGraph()
        wind.pgvolt = plots.voltGraph()
        wind.pgalti = plots.altiPlot()
        wind.pggyroPlot = plots.gyroPlot()
        
        wind.MRB = MRB()

        layout.addWidget(wind.pgtemp, 0, 0, 20, 20)
        layout.addWidget(wind.pgvolt, 20, 0, 20, 20)
        layout.addWidget(wind.pgalti, 0, 20, 20, 15)
        layout.addWidget(wind.pggyroPlot, 40, 0, 20, 20)
        layout.addWidget(wind.MRB, 20, 20)

        wind.show()
        wind.setWindowTitle('LivePlotting_W')
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('antialias',True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

