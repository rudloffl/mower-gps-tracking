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
from ftplib import FTP

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
    def __init__(self, gpspath='/dev/cu.usbserial', savingpath='/home/pi'):
        self.gpspath = gpspath
        self.savingpath = savingpath
        self.openserial()

    def openserial(self):
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

        while b'GPRMC' not in gpsentry:
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

    def tracking(self, ftptime=5, recordlength=10, onlyfinalftp=False):
        start = time.time()
        now = time.time()
        firstFixFlag = False
        while now-start < recordlength:
            gpsdata = self.get_coordinate()
            if gpsdata['validity'] == "A": # If the sentence shows that there's a fix, then we can log the line
                if firstFixFlag == False: # If we haven't found a fix before, then set the filename prefix with GPS date & time.
                    firstFixDate = gpsdata['fix_date'] + "-" + gpsdata['fix_time']
                    firstFixFlag = True
                    print('first fix done')
                else: # write the data to a simple log file and then the raw data as well:
                    print('recording file {}'.format(firstFixDate))
                    with open(firstFixDate +"-simple-log.txt", "a") as myfile:
                        myfile.write(gpsdata['fix_date'] + "-" +
                                     gpsdata['fix_time'] + "," +
                                     str(gpsdata['decimal_latitude']) + "," +
                                     str(gpsdata['decimal_longitude']) + "," +
                                     str(gpsdata['speed']) + ","
                                     "\n")
            #print(now)
            now = time.time()
            if (int(now - start) % ftptime == 0) and onlyfinalftp:
                print('ftpsaving')
                self.ftprecord(firstFixDate +"-simple-log.txt")
        self.ftprecord(firstFixDate +"-simple-log.txt")

        self.closeserial()

    def ftprecord(self, filename):
        with FTP("192.168.1.15") as ftp:
            ftp.login()
            ftp.cwd('dropinthenas')
            #print(ftp.getwelcome())
            #filename = 'test.txt'
            ftp.storbinary('STOR '+filename, open(filename, 'rb'))
            #print(ftp.dir())



if __name__ == '__main__':
    gpslogger = Gpslogger()
    #gpslogger.closeserial()
    gpslogger.tracking()
    #print(gpslogger.get_coordinate())
