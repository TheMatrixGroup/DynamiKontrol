import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

module = Module(debug=True)

module.motor.speed(1000)
print(module.motor.get_speed())

module.disconnect()
