import sys, time
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

module = Module()

def callback(string, angle):
    print(string)
    module.motor.angle(angle)

module.switch.press(callback, kwargs={'string': 'Switched to on', 'angle': 85})
module.switch.release(callback, args=('Switched to off', 0,))

while True:
    time.sleep(1)

module.disconnect()
