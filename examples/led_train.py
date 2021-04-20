from dynamikontrol import Module
import time

module = Module()

delay = 0.2 # LED를 켠 상태로 유지하는 시간(초)

while True:
    module.led.on(color='r') # 빨간색 LED를 켠다
    time.sleep(delay) # 기다린다

    module.led.off(color='r') # 빨간색 LED를 끈다
    module.led.on(color='y') # 노란색 LED를 켠다
    time.sleep(delay) # 기다린다

    module.led.off(color='y') # 노란색 LED를 끈다
    module.led.on(color='g') # 초록색 LED를 켠다
    time.sleep(delay) # 기다린다

    module.led.off(color='g') # 초록색 LED를 끈다

module.disconnect()
