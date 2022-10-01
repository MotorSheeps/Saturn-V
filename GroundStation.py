# SATURN V
# GGROUND STATION CODE
# FORMAT: TEAM_ID, MISSION_TIME, PACKET_COUNT, SW_STATE, PL_STATE, ALTITUDE, TEMP, VOLTAGE, GPS_LATITUDE, GPS_LONGITUDE, GYRO_R, GYRO_P, GYRO_Y

# TO DO LIST (No Order)
# Verify structure of packets
# Open and write to a CSV file
# Confirm serial is open
# Somehow make sure data is formatted correctly and handle errors

import serial # pip install serial
import PyQt5 #py -m pip install pyqt5
from digi.xbee.devices import XBeeDevice # py -m pip install digi-xbee
import time 
import threading


# instantiate xbee local node
xbee = XBeeDevice('COM3',9600) # might have to change COM location depending on computer

while xbee.open() == 0:
    xbee.open()

print('Connected')

# read data
message = xbee.read_data()
print(message)

#

