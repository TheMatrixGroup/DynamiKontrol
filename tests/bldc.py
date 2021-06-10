import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module
import time

module = Module(debug=True)

def func():
    print(time.time(), 'end')

module.motor.speed(4000, period=10, func=func)

for i in range(10):
    time.sleep(1)
    print(time.time(), i+1)
    print(module.motor.get_speed())

print('stop')

module.motor.stop()

module.disconnect()
