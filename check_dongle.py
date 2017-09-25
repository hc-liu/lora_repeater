#!/usr/bin/python

import os
import json
import sys
import time
import serial
import logging

USB_DEV_ARRAY = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3", "/dev/ttyUSB4", "/dev/ttyUSB5",
                 "/dev/ttyUSB6"]

def check_lora_module(dev_path):
    try:
        ser = serial.Serial(dev_path, 9600, timeout=0.5)
        ser.flushInput()
        ser.flushOutput()
        check_my_dongle = ser.readlines()
        ser.write("AT\n")
        check_my_dongle = ser.readlines()
        if any(REPLY_OK_STRING in s for s in check_my_dongle):
            print('My USB dongle checked')
            return ser
        else:
            return None
    except serial.serialutil.SerialException:
        # print 'FAIL: Cannot open Serial Port (No LoRa Node Inserted)'
        return None

global_check_dongle_exist = False
for devPath in USB_DEV_ARRAY:
    #print devPath
    ser = check_lora_module(devPath)
    if ser is None:
        continue
    else:
        global_check_dongle_exist = True
        print('Open LoRa node done:')
        print(devPath)
        break

if global_check_dongle_exist is False:
    print('no device be detected, exit!!!')
    sys.exit()