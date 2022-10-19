# SATURN V
# GROUND STATION CODE

import serial 
import sys  
import os
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice,XBee64BitAddress 
from time import sleep
import numpy as np
from random import randint
from digi.xbee.devices import DigiPointDevice, RemoteDigiPointDevice, XBee64BitAddress
from digi.xbee.models.options import DiscoveryOptions
from digi.xbee.models.status import NetworkDiscoveryStatus
import threading 
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication)
from PyQt5 import QtWidgets, QtCore, QtGui
import PyQt5
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# some parameters
xi = 2
maxRange = 60
packetInterval = 1000 #time in milliseconds between updates
counter = 0
split_data = []

# setting up local and remote xbee
houston = DigiPointDevice('COM3', 9600)
houston.open()
saturn = RemoteDigiPointDevice(houston, XBee64BitAddress.from_hex_string("0013A2004199938C"))



# network discovery
network = houston.get_network()
network.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF, DiscoveryOptions.APPEND_DD})
network.set_discovery_timeout(10)
network.clear()



# defining callbacks
# device discovered callback
def device_discovered_callback(xbee):
    print("Device discovered: %s" % xbee)

# Callback for discovery finished.
def discovery_completed_callback(discovery):
    if discovery == NetworkDiscoveryStatus.SUCCESS:
        print("Discovery process completed successfully.")
    else:
        print("An error occurred while discovering devices: %s" % discovery.description)

# data received callback
def data_received_callback(message):
    global parsed
    #print("From %s >> %s" % (message.remote_device.get_64bit_addr(),
                             #message.data.decode("latin-1")))

    line = message.data.decode("latin-1")
    parsed = line.split(",")
    filename = open("flight.csv", 'a')
    filename.write(str(parsed))
    filename.close()
    return parsed
    


# adding the callback
network.add_device_discovered_callback(device_discovered_callback)
network.add_discovery_process_finished_callback(discovery_completed_callback)



# starting discovery process
network.start_discovery_process()
print('Starting discovery process')
while network.is_discovery_running():
    sleep(0.5)



# manual release
class MRB(QtWidgets.QPushButton): #MRB = manual release button

    def manualRelease(MRB):
        print('Manually Releasing...')
    
    def __init__(MRB):

        QtWidgets.QPushButton.__init__(MRB)

        MRB.setText('⚠\nEJECT\n⚠')
        MRB.setToolTip('WARNING: EMERGENCY ONLY')
        MRB.setStyleSheet('background-color : red')
        MRB.setFont(QFont('Arial', 25))
        MRB.setGeometry(10,10,175,175)
        MRB.clicked.connect(MRB.manualRelease)



# defining graphs
packets = []
err_out_of_bounds = "SIM ERR: attempted to retrieve a packet out of profile's bounds"

pg.setConfigOption('background', (0, 0, 0))
pg.setConfigOption('foreground', (197, 198, 199))
# Interface variables
app = QApplication([])
view = pg.GraphicsView()
layout = pg.GraphicsLayout()
view.setCentralItem(layout)
view.show()
view.setWindowTitle('Saturn V Data')
view.resize(1200, 700)
# Fonts for text items
font = QFont()
font.setPixelSize(90)

# title
text = "DROP Ground Station"
layout.addLabel(text, col=1, colspan=21)
layout.nextRow()

# vertical Label
layout.addLabel('Space Hardware Club', angle=-90, rowspan=3)
layout.nextRow()



# altitude graph
l1 = layout.addLayout(colspan=20, rowspan=2)
l11 = l1.addLayout(rowspan=1, border=(83, 83, 83))
p1 = l11.addPlot(title="Altitude (m)")
altitude_plot = p1.plot(pen=(0, 119, 200))
altitude_data = np.linspace(0, 0, 30)
ptr1 = 0


def update_altitude(ALT):
    global altitude_plot, altitude_data, ptr1
    altitude_data[:-1] = altitude_data[1:]
    altitude_data[-1] = float(ALT)
    ptr1 += 1
    altitude_plot.setData(altitude_data)
    altitude_plot.setPos(ptr1, 0)



# temperature graph
l3 = layout.addLayout(colspan=20, rowspan=2)
l31 = l3.addLayout(rowspan=1, border=(83, 83, 83))
p2 = l31.addPlot(title="Temperature (°C)")
temperature_plot = p2.plot(pen=(0, 119, 200))
temperature_data = np.linspace(0, 0, 30)
ptr2 = 0


def update_temperature(TEMP):
    global temperature_plot, temperature_data, ptr2
    temperature_data[:-1] = temperature_data[1:]
    temperature_data[-1] = float(TEMP)
    ptr2 += 1
    temperature_plot.setData(temperature_data)
    temperature_plot.setPos(ptr2, 0)



# voltage graph
l4 = layout.addLayout(colspan=20, rowspan=2)
l41 = l4.addLayout(rowspan=1, border=(83, 83, 83))
p3 = l41.addPlot(title="Voltage (V)")
voltage_plot = p3.plot(pen=(0, 119, 200))
voltage_data = np.linspace(0, 0, 30)
ptr3 = 0


def update_voltage(VOLT):
    global voltage_plot, voltage_data, ptr3
    voltage_data[:-1] = voltage_data[1:]
    voltage_data[-1] = float(VOLT)
    ptr3 += 1
    voltage_plot.setData(voltage_data)
    voltage_plot.setPos(ptr3, 0)



# gyroscope graph
l5 = layout.addLayout(colspan=20, rowspan=2)
l51 = l5.addLayout(rowspan=1, border=(83, 83, 83))
p4 = l51.addPlot(title="Gyroscope (°/s)")
gyroscope_plot = p4.plot(pen=(0, 119, 200))
gyroscope_data = np.linspace(0, 0, 30)
ptr4 = 0


def update_gyroscope(GYROR,GYROP,GYROY):
    global gyroscope_plot, gyroscope_data, ptr4
    gyroscope_data[:-1] = gyroscope_data[1:]
    gyroscope_data[-1] = float(GYROR,GYROP,GYROY)
    ptr4 += 1
    gyroscope_plot.setData(gyroscope_data)
    gyroscope_plot.setPos(ptr4, 0)



# time, battery and free fall graphs
l2 = layout.addLayout(colspan=20, rowspan=2)
l21 = l2.addLayout(rowspan=1, border=(83, 83, 83))



# time graph
time_graph = l21.addPlot(title="Time Display")
time_graph.hideAxis('bottom')
time_graph.hideAxis('left')
time_text = pg.TextItem("test", anchor=(0.5, 0.5), color=(0, 119, 200))
time_text.setFont(font)
time_graph.addItem(time_text)


def update_time(TIME):
    global time_text
    time_text.setText(str(TIME))



# State Display
l2.nextRow()
l22 = l2.addLayout(rowspan=1, border=(83, 83, 83))
state_graph = l22.addPlot(title="State Display: ")
state_graph.hideAxis('bottom')
state_graph.hideAxis('left')
state_text = pg.TextItem("test", anchor=(0.5, 0.5), color=(0, 119, 200))
state_text.setFont(font)
state_graph.addItem(state_text)


def update_state(STATE):
    global state_text
    state_text.setText(str(STATE))



layout.nextRow()
layout.nextRow()
style = "background-color:rgb(0, 119, 200);color:rgb(0,0,0);font-size:14px;"
enable = False
activate = False



def drop_buttonPushed():
    houston.send_data(saturn, "DROP")
    print("Manually releasing...")


def gs_bottonPushed():
    houston.close()
    print("GCS closed")
    exit()



# buttons
button_layout = layout.addLayout(colspan=21)
button_spot = button_layout.addLayout(rowspan=1, border=(83, 83, 83))
button_spot.nextRow()
proxy = QGraphicsProxyWidget()
drop_button = QPushButton('Drop Device')
drop_button.setStyleSheet(style)
drop_button.clicked.connect(drop_buttonPushed)
proxy.setWidget(drop_button)
button_spot.addItem(proxy)
button_spot.nextCol()

proxy2 = QGraphicsProxyWidget()
gs_button = QPushButton('GCS Off')
gs_button.setStyleSheet(style)
gs_button.clicked.connect(gs_bottonPushed)
proxy2.setWidget(gs_button)
button_spot.addItem(proxy2)
button_spot.nextCol()


def update():
    houston.add_data_received_callback(data_received_callback)
    try:
        TIME = parsed[1]
        update_time(TIME)
        ALT = parsed[5]
        update_altitude(ALT)
        STATE = parsed[4]
        update_state(STATE)
        TEMP = parsed[6]
        update_temperature(TEMP)
        VOLT = parsed[7]
        update_voltage(VOLT)
        GYROR = parsed[8]
        GYROP = parsed[9]
        GYROY = parsed[10]

    except IndexError:
        print('Awaiting Packet')


if 1:
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(250)


if __name__ == '__main__':

    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()


input("Waiting for data...\n")
houston.close()