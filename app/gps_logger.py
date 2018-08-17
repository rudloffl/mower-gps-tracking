#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 5 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

import time

from modules.controler import LEDplus, Buttonplus
from modules.gps_mng import Gpslogger
from modules.uploadfiles import Networkmng


def waitrelease(button):
    while button.pressed:
        print('waiting...')
        time.sleep(.1)

def ledstandby():
    green.off()
    orange.blink()
    red.off()

def ledrecording():
    green.blink()
    orange.off()
    red.off()

def lederrorftp():
    red.blink()
    orange.blink()
    green.blink()

def ledsuccessftp():
    red.on()
    orange.off()
    green.on()


if __name__ == '__main__':
    green = LEDplus(18)
    orange = LEDplus(17)
    red = LEDplus(27)

    button1 = Buttonplus(22)
    button2 = Buttonplus(23)

    gpslogger = Gpslogger()

    ftpsav = Networkmng()

    ledstandby()

    while True:
        time.sleep(.1)

        if button1.pressed:
            if gpslogger.recording == False:
                waitrelease(button1)
                gpslogger.tracking()
                ledrecording()

            elif gpslogger.recording == True:
                gpslogger.stop_tracking()
                waitrelease(button1)
                ledstandby()


        if button2.pressed:
            if gpslogger.recording == True:
                red.blink()
                waitrelease(button2)
                red.off()
            elif gpslogger.recording == False:
                red.blink()
                orange.off()
                green.off()
                waitrelease(button2)
                ftpresponse = ftpsav.uploadall() #True if error

                if ftpresponse: #There was an issue during for the FTP transfer
                    lederrorftp()
                    time.sleep(5)
                    ledstandby()
                else: #No problem
                    ledsuccessftp()
                    time.sleep(2)
                    ledstandby()
