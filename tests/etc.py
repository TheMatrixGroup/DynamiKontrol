import sys, time
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

m = Module(debug=True)

# Print module serial number
print('Serial number: %s' % (m.get_serial_no(),))

print('ID: %s' % (m.get_id(), ))

print('Device time: %s' % (m.get_time(), ))

print('FW version: %s' % (m.get_fw_version(),))

m.disconnect()
