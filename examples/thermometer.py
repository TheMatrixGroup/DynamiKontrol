from dynamikontrol import Module
import requests, time
from datetime import datetime

module = Module()

# weather of Seoul, Korea
url = 'https://fcc-weather-api.glitch.me/api/current?lat=37.566536&lon=126.977966'

while True:
    res = requests.get(url).json()
    temp = res['main']['temp']

    print(f'{datetime.now()} temperature {temp}')

    angle = int(temp * 45 / 30)
    module.motor.angle(angle)

    time.sleep(60)

module.disconnect()
