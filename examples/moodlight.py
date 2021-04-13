from dynamikontrol import Module
import time

module = Module()

while True:
    for i in range(100):
        module.base_led.mix(rgb=(i, i, 100-i))
        time.sleep(0.01)

    for i in range(100):
        module.base_led.mix(rgb=(100-i, 100-i, i))
        time.sleep(0.01)
