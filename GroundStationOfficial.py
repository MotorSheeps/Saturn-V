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
counter = 0
split_data = []

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
# device discovered callback
def device_discovered_callback(xbee):
    print("Device discovered: %s" % xbee)

# Callback for discovery finished.
def discovery_completed_callback(discovery):
    if discovery == NetworkDiscoveryStatus.SUCCESS:
        print("Discovery process completed successfully.")
    else:
        print("An error occurred while discovering devices: %s" % discovery.description)


# need for next callback and graphs
parsed = []
err_out_of_bounds = "SIM ERR: attempted to retrieve a packet out of profile's bounds"



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



# defining graphs
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
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
text = "Houston Ground Station"
#layout.addLabel(text, col=1, colspan=21)
layout.nextRow()

# vertical Label
#layout.addLabel('Space Hardware Club', angle=-90, rowspan=3)
layout.nextRow()



# altitude graph
l1 = layout.addLayout(col = 1, row = 1, colspan=20, rowspan=1)
p1 = l1.addPlot(title="Altitude (m)")
altitude_plot = p1.plot(pen='k')
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
l3 = layout.addLayout(col = 21, row = 1, colspan=20, rowspan=1)
p2 = l3.addPlot(title="Temperature (°C)")
temperature_plot = p2.plot(pen='k')
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
l4 = layout.addLayout(col = 21, row = 2, colspan=20, rowspan=1)
p3 = l4.addPlot(title="Voltage (V)")
voltage_plot = p3.plot(pen='k')
voltage_data = np.linspace(0, 0, 30)
ptr3 = 0


def update_voltage(VOLT):
    global voltage_plot, voltage_data, ptr3
    voltage_data[:-1] = voltage_data[1:]
    voltage_data[-1] = float(VOLT)
    ptr3 += 1
    voltage_plot.setData(voltage_data)
    voltage_plot.setPos(ptr3, 0)



# gyroscope graphs
# roll
l5 = layout.addLayout(col = 1, row = 2, colspan=20, rowspan=1)
p4 = l5.addPlot(title="Gyroscope")
gyroscope_plotR = p4.plot(pen='k')
gyroscope_dataR = np.linspace(0, 0, 30)
ptr4 = 0


def update_gyroscopeR(GYROR):
    global gyroscope_plotR, gyroscope_dataR, ptr4
    gyroscope_dataR[:-1] = gyroscope_dataR[1:]
    gyroscope_dataR[-1] = float(GYROR)
    ptr4 += 1
    gyroscope_plotR.setData(gyroscope_dataR)
    gyroscope_plotR.setPos(ptr4, 0)

# pitch
gyroscope_plotP = p4.plot(pen='r')
gyroscope_dataP = np.linspace(0, 0, 30)
ptr5 = 0


def update_gyroscopeP(GYROP):
    global gyroscope_plotP, gyroscope_dataP, ptr5
    gyroscope_dataP[:-1] = gyroscope_dataP[1:]
    gyroscope_dataP[-1] = float(GYROP)
    ptr5 += 1
    gyroscope_plotP.setData(gyroscope_dataP)
    gyroscope_plotP.setPos(ptr5, 0)

# yaw
gyroscope_plotY = p4.plot(pen=(0, 145, 255))
gyroscope_dataY = np.linspace(0, 0, 30)
ptr6 = 0


def update_gyroscopeY(GYROY):
    global gyroscope_plotY, gyroscope_dataY, ptr6
    gyroscope_dataY[:-1] = gyroscope_dataY[1:]
    gyroscope_dataY[-1] = float(GYROY)
    ptr6 += 1
    gyroscope_plotY.setData(gyroscope_dataY)
    gyroscope_plotY.setPos(ptr6, 0)



# time, battery and free fall graphs
l21 = layout.addLayout(col = 41, row = 1, colspan=15, rowspan=1)

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
l22 = layout.addLayout(col = 41, row = 2, rowspan=1, border=(83, 83, 83))
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
drop_button = QPushButton('⚠\nEJECT\n⚠')
drop_button.setStyleSheet('background-color : red')
drop_button.setFont(QFont('Arial', 18))
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
        update_gyroscopeR(GYROR)
        GYROP = parsed[9]
        update_gyroscopeP(GYROP)
        GYROY = parsed[10]
        update_gyroscopeY(GYROY)

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
