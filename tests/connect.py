import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

m = Module(debug=True)

m.disconnect()
