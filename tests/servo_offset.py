import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module
import time

module = Module(debug=True)

while True:
    print(module.motor.get_offset())

    time.sleep(2)

    module.motor.set_offset(17.5)
