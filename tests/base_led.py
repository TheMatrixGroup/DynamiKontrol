import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module, BaseLED
import time

module = Module(debug=True)
base_led = module.base_led

# Mix
start_time = time.time()
while True:
    if time.time() - start_time > 5:
        break

    for i in range(100):
        base_led.mix(rgb=(i, i, 100-i))
        time.sleep(0.02)

    for i in range(100):
        base_led.mix(rgb=(100-i, 100-i, i))
        time.sleep(0.02)

# All on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    base_led.on(color='all')
    time.sleep(0.1)

    base_led.off(color='all')
    time.sleep(0.1)

# Red on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    base_led.on(color='r')
    time.sleep(0.1)

    base_led.off(color='r')
    time.sleep(0.1)

# Yellow on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    base_led.on(color='g')
    time.sleep(0.1)

    base_led.off(color='g')
    time.sleep(0.1)

# Green on - off
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    base_led.on(color='b')
    time.sleep(0.1)

    base_led.off(color='b')
    time.sleep(0.1)

# Toggle
start_time = time.time()
while True:
    if time.time() - start_time > 3:
        break

    base_led.toggle(color='all')
    time.sleep(0.1)

time.sleep(3)

module.disconnect()
