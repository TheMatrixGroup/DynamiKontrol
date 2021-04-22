import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module

with Module(debug=True) as module:
    module.set_default_switch_operation(on=False)
