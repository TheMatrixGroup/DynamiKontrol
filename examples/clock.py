from dynamikontrol import Module
import time

module = Module()

while True:
    second = int(time.time() % 60)

    angle = (second - 30) * 2

    module.motor.angle(angle)

    print(second)

    time.sleep(1)

module.disconnect()
