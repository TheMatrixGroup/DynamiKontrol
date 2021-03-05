import sys
sys.path.insert(0, '../dynamikontrol')

from dynamikontrol import Module, Timer
import time

t1 = Timer()
t2 = Timer()

module = Module(debug=True)

t1.callback_at(func=module.led.toggle, args=('r',), at='2021-03-02 19:46:30', interval=0.1)

t2.callback_after(func=module.led.toggle, args=('g',), after=1, interval=0.1)

time.sleep(5)

t1.stop()
t2.stop()

module.disconnect()
