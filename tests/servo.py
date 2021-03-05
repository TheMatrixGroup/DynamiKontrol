import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module
import time

module = Module(debug=True)

module.motor.angle(0)
time.sleep(2)

start_time = time.time()

while True:
    if time.time() - start_time > 60:
        break

    # module.motor.angle(40)
    # time.sleep(1.2)

    # module.motor.angle(0)
    # time.sleep(1.2)

    # module.motor.angle(-40)
    # time.sleep(1.2)

    # module.motor.angle(0)
    # time.sleep(1.2)

    module.motor.planning(50, 5000)
    time.sleep(5.2)
    
    module.motor.planning(-50, 5000)
    time.sleep(5.2)
module.disconnect()
