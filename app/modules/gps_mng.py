#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 5 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

import serial
import os
import time
import threading


def degrees_to_decimal(data, hemisphere):
    try:
        decimalPointPosition = data.index('.')
        degrees = float(data[:decimalPointPosition-2])
        minutes = float(data[decimalPointPosition-2:])/60
        output = degrees + minutes
        if hemisphere is 'N' or hemisphere is 'E':
            return output
        if hemisphere is 'S' or hemisphere is 'W':
            return -output
    except:
        return "ERROR"

class Gpslogger():
    def __init__(self, gpspath='/dev/ttyUSB0', savingpath='/home/pi'):
        #gpspath = '/dev/cu.usbserial' #dirty fix to run on coding computer
        #savingpath = '' #another dirty trick...
        threading.Thread.__init__(self)
        self.gpspath = gpspath
        self.savingpath = savingpath
        self.recording = False

    def openserial(self):
        print('serial port creation')
        self.ser = serial.Serial(self.gpspath,
                   baudrate=4800,
                   timeout=1, #1
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   bytesize=serial.EIGHTBITS
                  )

    def closeserial(self):
        self.ser.close()

    def get_coordinate(self, maxattempt=100):
        gpsentry = b''
        #print('attempt to get entry')
        while b'GPRMC' not in gpsentry:
            time.sleep(.1)
            gpsentry = self.ser.readline()

        #print('entry caught --> {}'.format(gpsentry))
        gpsdata = self.parse_GPRMC(gpsentry)
        return gpsdata

    def parse_GPRMC(self, data):
        data = data.split(b',')
        dict = {
                'fix_time': data[1].decode('ascii').split('.')[0],
                'validity': data[2].decode('ascii'),
                'latitude': data[3].decode('ascii'),
                'latitude_hemisphere' : data[4].decode('ascii'),
                'longitude' : data[5].decode('ascii'),
                'longitude_hemisphere' : data[6].decode('ascii'),
                'speed': data[7].decode('ascii'),
                'true_course': data[8].decode('ascii'),
                'fix_date': data[9].decode('ascii'),
                'variation': data[10].decode('ascii'),
                'variation_e_w' : data[11].decode('ascii'),
                'checksum' : data[12].decode('ascii')
                }
        dict['decimal_latitude'] = degrees_to_decimal(dict['latitude'], dict['latitude_hemisphere'])
        dict['decimal_longitude'] = degrees_to_decimal(dict['longitude'], dict['longitude_hemisphere'])
        #print(dict)
        return dict

    def stop_tracking(self):
        self.recording = False
        self.__threading.join()

    def tracking(self):
        self.recording = True
        self.__threading = threading.Thread(target=self.__tracking)
        self.__threading.start()

    def __tracking(self,):
        self.openserial()
        print('Tracking starts')
        firstFixFlag = False
        while self.recording:
            time.sleep(.1)
            gpsdata = self.get_coordinate()
            if gpsdata['validity'] == "A": # If the sentence shows that there's a fix, then we can log the line
                if firstFixFlag == False: # If we haven't found a fix before, then set the filename prefix with GPS date & time.
                    firstFixDate = gpsdata['fix_date'] + "-" + gpsdata['fix_time']
                    firstFixFlag = True
                    print('first fix done')
                else: # write the data to a simple log file and then the raw data as well:
                    print('recording file {}'.format(firstFixDate))
                    with open(os.path.join(self.savingpath,firstFixDate+"-simple-log.txt"), "a") as myfile:
                        myfile.write(gpsdata['fix_date'] + "-" +
                                     gpsdata['fix_time'] + "," +
                                     str(gpsdata['decimal_latitude']) + "," +
                                     str(gpsdata['decimal_longitude']) + "," +
                                     str(gpsdata['speed']) + ","
                                     "\n")

        self.closeserial()

if __name__ == '__main__':
    gpslogger = Gpslogger()
    print('tracker created')
    gpslogger.tracking()
    print('recording start')
    time.sleep(10)
    gpslogger.stop_tracking()
    print('recording end')
