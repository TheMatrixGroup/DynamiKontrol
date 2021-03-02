import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module, Servo
import time

module = Module(debug=True)
servo = Servo(module=module)

servo.angle(0)
time.sleep(2)

start_time = time.time()

while True:
    if time.time() - start_time > 10:
        break

    servo.angle(10)
    time.sleep(2)

    servo.angle(-10)
    time.sleep(2)

module.disconnect()
