import sys, time
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

m = Module(debug=True)

# Print module serial number
print('Serial number: %s' % (m.get_serial_no(),))

m.led.blink(color='g', on_interval=1000, off_interval=100)

m.disconnect()
