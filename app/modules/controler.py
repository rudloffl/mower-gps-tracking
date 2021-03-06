#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 5 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

import time
import threading
from gpiozero import LED, Button

class LEDplus():
    def __init__(self,pinnumber):
        self.led = LED(pinnumber)
        self.led.off()
        self.__loop = False
        self.__threading = threading.Thread(target=self.__blink, args=(.5, ))

    def on(self,):
        self.__loop = False
        self.maybejoin()
        self.led.on()

    def off(self, ):
        self.__loop = False
        self.maybejoin()
        self.led.off()

    def maybejoin(self):
        if self.__threading.is_alive():
            self.__threading.join()

    def blink(self):
        self.__loop = True
        self.__threading = threading.Thread(target=self.__blink, args=(.5, ))
        self.__threading.start()

    def __blink(self, pitch=.5):
        while self.__loop:
            self.led.on()
            time.sleep(pitch/2)
            self.led.off()
            time.sleep(pitch/2)

class Buttonplus():
    def __init__(self, pinnumber):
        self.button = Button(pinnumber)
        self.pinnumber = pinnumber
        self.__loop = True
        self.__threading = threading.Thread(target=self.__watch)
        self.__threading.start()
        self.pressed = False

    def __watch(self):
        while self.__loop:
            time.sleep(.1)
            if self.button.is_pressed and self.pressed == False:
                print("Button (GPIO {}) is pressed".format(self.pinnumber))
                self.pressed = True
            elif self.pressed == True and not self.button.is_pressed:
                print("Button (GPIO {}) is released".format(self.pinnumber))
                self.pressed = False

def test1():
    while True:
        time.sleep(.1)
        if button1.pressed == True:
            green.on()
            orange.on()
            red.on()

            time.sleep(1)

            green.blink()
            orange.blink()
            red.blink()

            time.sleep(3)

            green.on()
            orange.on()
            red.on()

            time.sleep(5)

            green.off()
            orange.off()
            red.off()


if __name__ == '__main__':
    green = LEDplus(18)
    orange = LEDplus(17)
    red = LEDplus(27)
    button1 = Buttonplus(22)
    button2 = Buttonplus(23)
    print('#############\n### READY ###\n#############')

    test1()
