from dynamikontrol import Module
import time, random

module = Module()

direction = 1 # initial direction, clockwise
start_time = time.time()
stop_time = 5 # stop after 5 seconds
stop_angle = random.randint(-80, 80) # random angle

while True:
    if time.time() - start_time > stop_time:
        module.motor.angle(angle=stop_angle)
        print(f'Motor stopped at {stop_angle} degree')
        break

    direction = direction * -1 # change direction
    module.motor.angle(angle=direction * 80)
    time.sleep(0.6)

module.led.blink()
module.disconnect()
