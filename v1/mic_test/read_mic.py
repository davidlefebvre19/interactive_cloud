#!/usr/bin/python

import sys
import usb.core
import requests
import time

dev=usb.core.find(idVendor=0x16c0,idProduct=0x5dc)

assert dev is not None

print(dev)

print (hex(dev.idVendor)+','+hex(dev.idProduct))

try:
    while True:
        time.sleep(0.1)
        ret = dev.ctrl_transfer(0xC0,4,0,0,200)
        dB = (ret[0]+((ret[1]&3)*256))*0.1+30
        print (dB)
        msg="{'dB':'"+str(dB)+"'}"
except KeyboardInterrupt:
    print("Exiting program...")