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

    module.base_led.on(color='all')
    time.sleep(0.1)

    module.base_led.off(color='all')
    time.sleep(0.1)

# Red on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.base_led.on(color='r')
    time.sleep(0.1)

    module.base_led.off(color='r')
    time.sleep(0.1)

# Yellow on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.base_led.on(color='g')
    time.sleep(0.1)

    module.base_led.off(color='g')
    time.sleep(0.1)

# Green on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.base_led.on(color='b')
    time.sleep(0.1)

    module.base_led.off(color='b')
    time.sleep(0.1)

# Toggle
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    module.base_led.toggle(color='all')
    time.sleep(0.1)

module.disconnect()
