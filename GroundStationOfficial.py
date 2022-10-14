# SATURN V
# GROUND STATION CODE
# FORMAT: TEAM_ID, MISSION_TIME, PACKET_COUNT, SW_STATE, PL_STATE, ALTITUDE, TEMP, VOLTAGE, GPS_LATITUDE, GPS_LONGITUDE, GYRO_R, GYRO_P, GYRO_Y


import serial 
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  
import os
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice,XBee64BitAddress 
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication)
from PyQt5 import QtWidgets, QtCore
from time import sleep
import numpy as np
from random import randint
from digi.xbee.devices import DigiPointDevice, RemoteDigiPointDevice, XBee64BitAddress
from digi.xbee.models.options import DiscoveryOptions
from digi.xbee.models.status import NetworkDiscoveryStatus


# setting up local and remote xbee
houston = DigiPointDevice('COM3', 9600)
houston.open()
saturn = RemoteDigiPointDevice(houston, XBee64BitAddress.from_hex_string("0013A2004199938C"))



# network discovery
network = houston.get_network()
network.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF, DiscoveryOptions.APPEND_DD})
network.set_discovery_timeout(10)
network.clear()



# defining graphs
# NOTE: need to go in and fix data to parse through data received
class tempPlot(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        
        self.x = list(range(-101,-1))
        self.y = [randint(0,0) for _ in range(100)]

        self.setLabel("left", "Temperature (°C)")
        self.setLabel("bottom", "Second (S)")
        self.setTitle('Temperature')

        self.tempLine = self.plot(self.x, self.y, pen='purple')
        
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
        self.setTitle('Pressure')

        self.presLine = self.plot(self.x, self.y, pen='gray')
        
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
        self.setTitle('Altitude')

        self.altiLine = self.plot(self.x, self.y, pen='w')
        
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



# defining callbacks
# data received callback
def data_received_callback(message):
    address = message.remote_device.get_64bit_addr()
    data = message.data.decode("utf8")
    print("Received data from %s: %s" % (address, data))

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
houston.add_data_received_callback(data_received_callback)



# starting discovery process
network.start_discovery_process()
print('Starting discovery process')
while network.is_discovery_running():
    sleep(1)



# preparing for data NOTE: ISSUE
input("Waiting for data...\n")
houston.close()



# handling data once received
while True:
    message = houston.read_data()
    if houston.read_data():
        print(message)
        if __name__ == '__main__':
            app = QApplication(sys.argv)
            window = Window()

    # need to parse through data for graphs

    # TEAM_ID, MISSION_TIME, PACKET_COUNT, SW_STATE, PL_STATE, ALTITUDE, TEMP, VOLTAGE, 
    # GPS_LATITUDE, GPS_LONGITUDE, GYRO_R, GYRO_P, GYRO_Y
    filename = open("flight.csv", 'a')
    filename.write("example\n")
    filename.close()

    # NOTE: i don't think this is working the way i want. we need threads
   


   
# NOTE:     
# should be issue with arudiono code
# need to fix the issue 

