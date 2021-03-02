import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module, LED
import time

module = Module(debug=True)

start_time = time.time()

while True:
    if time.time() - start_time > 3:
        break

    module.LED.on(id=0)
    time.sleep(0.1)

    module.LED.off(id=0)
    time.sleep(0.1)

module.disconnect()
