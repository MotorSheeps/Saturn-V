#XBee
import digi.xbee
from digi.xbee.devices import DigiPointDevice, RemoteDigiPointDevice, XBee64BitAddress
from digi.xbee.models.options import DiscoveryOptions
from digi.xbee.models.status import NetworkDiscoveryStatus

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
from time import sleep
import sys
import os
from random import randint


xi = 2
maxRange = 60
packetInterval = 500 #time in milliseconds between updates
'''
#-----------------------------------------------------------------------------------------------
#  XBee SetUp
#-----------------------------------------------------------------------------------------------

# setting up local and remote xbee
houston = DigiPointDevice('COM7', 9600)
houston.open()
saturn = RemoteDigiPointDevice(houston, XBee64BitAddress.from_hex_string("0013A2004199938C"))



# network discovery
network = houston.get_network()
network.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF, DiscoveryOptions.APPEND_DD})
network.set_discovery_timeout(10)
network.clear()

# defining callbacks
# data received callback
def data_received_callback(message):
    print("From %s >> %s" % (message.remote_device.get_64bit_addr(),
                             message.data.decode("latin-1")))


# device discovered callback
def device_discovered_callback(xbee):
    print("Device discovered: %s" % xbee)

# Callback for discovery finished.
def discovery_completed_callback(discovery):
    if discovery == NetworkDiscoveryStatus.SUCCESS:
        print("Discovery process completed successfully.")
    else:
        print("An error occurred while discovering devices: %s" % discovery.description)



# adding the callbacksk
network.add_device_discovered_callback(device_discovered_callback)
network.add_discovery_process_finished_callback(discovery_completed_callback)


# starting discovery process
network.start_discovery_process()
print('Starting discovery process')
while network.is_discovery_running():
    sleep(0.5)

houston.add_data_received_callback(data_received_callback)


# preparing for data NOTE: ISSUE
#input("Waiting for data...\n")
#houston.close()



# handling data once received
while True:
    message = str(houston.read_data())
    parse = message.split(",")
    print(message)
    print(parse)
    sleep(0.999999)
    
    #app = QApplication(sys.argv)
    #window = Window()

    # need to parse through data for graphs

    # TEAM_ID, MISSION_TIME, PACKET_COUNT, SW_STATE, PL_STATE, ALTITUDE, TEMP, VOLTAGE, 
    # GPS_LATITUDE, GPS_LONGITUDE, GYRO_R, GYRO_P, GYRO_Y
packet = open("flight.csv", 'a')
packet.write(parse)
packet.close()'''

'''Packet delivers as [1005,MISIION_TIME,PACKET_COUNT,SW_STATE,PL_STATE,ALTITUDE,TEMP,
VOLTAGE,GYRO_R,GYRO_P,GYRO_Y]'''


'''
t = 1
p = 1
A = 500
T = randint(0,40)
V = randint(0,1)
R = randint(0,400)
P = randint(0,400)
Y = randint(0,400)'''

t = 0
p = 0
A = 0
T = 0
V = 0
R = 0
P = 0
Y = 0
        
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
            tempGraph.y = [0 for _ in range(xi)]
            tempGraph.storeY = [tempGraph.y[-1] for _ in range(xi)]
            tempGraph.avg = [0 for _ in range(len(tempGraph.x))]
            tempGraph.storeAvg = [0 for _ in range(len(tempGraph.x))]

            tempGraph.setLabel('left', 'Temperature (°C)')
            tempGraph.setLabel('bottom', 'Second (s)')
            tempGraph.setTitle('Temperature')
            tempGraph.setBackground('w')
            tempGraph.showGrid(x=True, y=True)
            tempGraph.addLegend()

            tempGraph.tempAvg = tempGraph.plot(tempGraph.x, tempGraph.storeAvg, name = 'Avg Temp', pen='b')
            tempGraph.tempLine = tempGraph.plot(tempGraph.x, tempGraph.y, name = 'Temp', pen='k')
        
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
                    tempGraph.avg.append(sum(tempGraph.storeY) / len(tempGraph.storeY))
                    tempGraph.tempAvg.setData(tempGraph.x, tempGraph.avg)
                else:
                    tempGraph.avg.append(sum(tempGraph.storeY) / len(tempGraph.storeY))
                    tempGraph.tempAvg.setData(tempGraph.x[11:], tempGraph.avg[11:])
                    
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
            voltGraph.setBackground('w')
            voltGraph.showGrid(x=True, y=True)

            voltGraph.voltLine = voltGraph.plot(voltGraph.x, voltGraph.y, pen='k')
            
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
            altiGraph.setYRange(0, 600, padding=0)
            altiGraph.setBackground('w')
            altiGraph.showGrid(x=True, y=True)

            altiGraph.altiLine = altiGraph.plot(altiGraph.x, altiGraph.y, pen='k')
            
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
        def __init__(gyroPlot):
            pg.PlotWidget.__init__(gyroPlot)
            
            gyroPlot.x = list(range(-(xi),0))
            gyroPlot.yR = [randint(0,0) for _ in range(xi)]
            gyroPlot.yP = [randint(0,0) for _ in range(xi)]
            gyroPlot.yY = [randint(0,0) for _ in range(xi)]

            gyroPlot.setLabel('left', 'details')
            gyroPlot.setLabel('bottom', 'Second (s)')
            gyroPlot.setTitle('Gyroscope')
            gyroPlot.setBackground('w')
            gyroPlot.showGrid(x=True, y=True)
            gyroPlot.addLegend()

            gyroPlot.gyroLineR = gyroPlot.plot(gyroPlot.x, gyroPlot.yR, name = 'Roll' , pen='r')
            gyroPlot.gyroLineP = gyroPlot.plot(gyroPlot.x, gyroPlot.yP, name = 'Pitch', pen='b')
            gyroPlot.gyroLineY = gyroPlot.plot(gyroPlot.x, gyroPlot.yY, name = 'Yaw'  , pen='k')
            gyroPlot.setBackground('w')
            gyroPlot.showGrid(x=True, y=True)
            
            gyroPlot.timer = QtCore.QTimer()
            gyroPlot.timer.setInterval(packetInterval)
            gyroPlot.timer.timeout.connect(gyroPlot.update_plot_data)
            gyroPlot.timer.start()

        def update_plot_data(gyroPlot):

            xi = len(gyroPlot.x)

            #packetUpdate.updater()

            if xi < maxRange:
                
                gyroPlot.x.append(gyroPlot.x[-1] + 1)
                gyroPlot.yR.append(packet[8])
                gyroPlot.yP.append(packet[9])
                gyroPlot.yY.append(packet[10])

            else:
                
                gyroPlot.x = gyroPlot.x[1:]
                gyroPlot.x.append(gyroPlot.x[-1] + 1)

                gyroPlot.yR = gyroPlot.yR[1:]
                gyroPlot.yP = gyroPlot.yP[1:]
                gyroPlot.yY = gyroPlot.yY[1:]
                gyroPlot.yR.append(packet[8])
                gyroPlot.yP.append(packet[9])
                gyroPlot.yY.append(packet[10])

            gyroPlot.gyroLineR.setData(gyroPlot.x, gyroPlot.yR)
            gyroPlot.gyroLineP.setData(gyroPlot.x, gyroPlot.yP)
            gyroPlot.gyroLineY.setData(gyroPlot.x, gyroPlot.yY)

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

        #console = PythonConsole()
        
        wind.pgtemp = plots.tempGraph()
        wind.pgvolt = plots.voltGraph()
        wind.pgalti = plots.altiPlot()
        wind.pggyro = plots.gyroPlot()
        
        wind.MRB = MRB()

        layout.addWidget(wind.pgtemp, 0, 0, 20, 20)
        layout.addWidget(wind.pgvolt, 20, 0, 20, 20)
        layout.addWidget(wind.pgalti, 0, 20, 20, 20)
        layout.addWidget(wind.pggyro, 20, 20, 20, 20)
        layout.addWidget(wind.MRB, 40, 0, 5, 5)

        wind.show()
        wind.setWindowTitle('Houston')
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('antialias',True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

