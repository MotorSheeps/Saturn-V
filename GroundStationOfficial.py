# SATURN V
# GROUND STATION CODE

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
input("Waiting for data...\n")
houston.close()



# handling data once received
while True:
    message = houston.read_data()
    parse = message.split(",")
    
    app = QApplication(sys.argv)
    window = Window()

    # need to parse through data for graphs

    # TEAM_ID, MISSION_TIME, PACKET_COUNT, SW_STATE, PL_STATE, ALTITUDE, TEMP, VOLTAGE, 
    # GPS_LATITUDE, GPS_LONGITUDE, GYRO_R, GYRO_P, GYRO_Y
    filename = open("flight.csv", 'a')
    filename.write(parse)
    filename.close()

    # NOTE: i don't think this is working the way i want. we need threads
   


   
# NOTE:     
# should be issue with arudiono code
# need to fix the issue 

