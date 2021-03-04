import sys, time
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

m = Module(debug=True)

time.sleep(2)

m.disconnect()
