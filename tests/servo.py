import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module
import time

module = Module(debug=True)

module.motor.angle(0)
time.sleep(2)

start_time = time.time()

while True:
    if time.time() - start_time > 10:
        break

    module.motor.angle(10)
    time.sleep(2)

    module.motor.angle(-10)
    time.sleep(2)

module.disconnect()
