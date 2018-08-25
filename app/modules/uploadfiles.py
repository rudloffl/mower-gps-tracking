#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 5 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

from ftplib import FTP
import os

class Networkmng():
    def __init__(self, IP_address = "192.168.1.15",
                    localpath='/home/pi',
                    savingpath='dropinthenas',):

        #localpath = '.'
        self.IP_address = IP_address
        self.localpath = localpath
        self.savingpath = savingpath


    def uploadall(self):
        #files = [os.path.abspath(os.path.join(self.localpath, file)) for file in os.listdir(self.localpath) if file.endswith('.csv')]
        files = [file for file in os.listdir(self.localpath) if file.endswith('.csv')]
        #print(files)

        if len(files)==0:
            return True

        try:
            for file in files:
                self.ftprecord(file)

            for file in [os.path.abspath(os.path.join(self.localpath, file)) for file in os.listdir(self.localpath) if file.endswith('.csv')]:
                os.remove(file)
                #print(file)
        except Exception as e:
            print('Oups... Something went wrong')
            return True

        return False


    def ftprecord(self, filename):
        with FTP("192.168.1.15") as ftp:
            ftp.login(user = 'user', passwd = 'passwd') #
            ftp.cwd(self.savingpath)
            ftp.storbinary('STOR '+filename, open(os.path.join(self.localpath, filename), 'rb'))
            #print(ftp.dir())


if __name__ == '__main__':
    networkmng = Networkmng()
    networkmng.uploadall()


/usr/bin/python3 /home/pi/mower-gps-tracking/app/gps_logger.py
