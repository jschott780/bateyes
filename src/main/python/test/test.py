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
import json
import datetime

devices = ['/dev/tty.usbserial-A40105TJ'
          ,'/dev/tty.usbserial-A800HGRA']
device = devices[0]

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv
        
def microsecondsToInches(microseconds):
    # According to Parallax's datasheet for the PING))), there are
    # 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
    # second).  This gives the distance traveled by the ping, outbound
    # and return, so we divide by 2 to get the distance of the obstacle.
    # See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
    return microseconds / 74 / 2;

def microsecondsToCentimeters(microseconds):
    # The speed of sound is 340 m/s or 29 microseconds per centimeter.
    # The ping travels out and back, so to find the distance of the
    # object we take half of the distance traveled.
    return microseconds / 29 / 2;


    
if __name__ == '__main__':
    
    print('connecting to xbee ' + device)
    port = serial.Serial( port=device,
                         baudrate=9600,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=1)


    # read data from serial port
    while True:
        jsonMsg = readlineCR(port)
        
        # ignore empty packets
        if ( len(jsonMsg) > 0 ):
            # parse the json
            try:
                packet = json.loads(jsonMsg,encoding="UTF-8")
            except:
                print "malformed json: " + jsonMsg
                jsonMsg = None
                
            # print the info
            if jsonMsg != None: 
                # convert the time into a distance
                d = datetime.datetime.now()
                nowDate = d.strftime('%Y-%m-%d %H:%M:%S %Z')
    
                duration = int(packet['ping'])
                inches = microsecondsToInches(duration);
      
                print "time: %s\tdist: %sin" % (nowDate,str(inches))
           
   
    print('closing port')
    port.close()
