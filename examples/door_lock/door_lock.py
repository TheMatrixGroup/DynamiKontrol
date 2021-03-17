from dynamikontrol import Module
from flask import Flask, request, render_template

module = Module()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change', methods=['POST'])
def change():
    is_locked = request.form['is_locked']

    if is_locked == 'true':
        module.motor.angle(85)
        module.led.off(color='r')
        module.led.on(color='g')
    else:
        module.motor.angle(-45)
        module.led.off(color='g')
        module.led.on(color='r')

    return {'result': True}

if __name__ == '__main__':
    app.run()
    module.disconnect()
