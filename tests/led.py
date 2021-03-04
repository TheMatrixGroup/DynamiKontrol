import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module
import time

module = Module(debug=True)

# All on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.led.on(color='all')
    time.sleep(0.1)

    module.led.off(color='all')
    time.sleep(0.1)

# Red on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.led.on(color='r')
    time.sleep(0.1)

    module.led.off(color='r')
    time.sleep(0.1)

# Yellow on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.led.on(color='y')
    time.sleep(0.1)

    module.led.off(color='y')
    time.sleep(0.1)

# Green on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.led.on(color='g')
    time.sleep(0.1)

    module.led.off(color='g')
    time.sleep(0.1)

# Toggle
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.led.toggle(color='all')
    time.sleep(0.1)

# Blink
module.led.blink(color='r', on_interval=1000, off_interval=100)
module.led.blink(color='y', on_interval=1000, off_interval=100)
module.led.blink(color='g', on_interval=1000, off_interval=100)
time.sleep(3)

module.disconnect()
