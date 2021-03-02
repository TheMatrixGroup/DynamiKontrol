import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module
import time

module = Module(debug=True)

start_time = time.time()

while True:
    if time.time() - start_time > 3:
        break

    module.led.on(id=0)
    time.sleep(0.1)

    module.led.off(id=0)
    time.sleep(0.1)

module.disconnect()
