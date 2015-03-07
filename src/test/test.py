#!/usr/bin/python
"""
Continuously read the serial port and process IO data received from a remote XBee.
https://code.google.com/p/python-xbee/
@author: schottj
"""

import serial
import time
import sys
import io

devices = ['/dev/tty.usbserial-A40105TJ'
          ,'/dev/tty.usbserial-A800HGRA']
device = devices[1]




def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv
        
if __name__ == '__main__':
    
    print('connecting to xbee ' + device)
    port = serial.Serial( port=device,
                         baudrate=9600,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=1)


    while True:
        rcv = readlineCR(port)
        if ( len(rcv) > 0 ):
            print("-->" + rcv)
   
    print('closing port')
    port.close()
