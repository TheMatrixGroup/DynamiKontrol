import sys, time
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

module = Module()

time.sleep(1)

def cb():
    print('hello')

module.motor.angle(angle=85, func=cb)

time.sleep(10)

module.disconnect()
