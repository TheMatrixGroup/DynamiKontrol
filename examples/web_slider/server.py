from dynamikontrol import Module
from flask import Flask, request, render_template

module = Module()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change', methods=['POST'])
def change():
    volume = int(request.form['volume'])

    module.motor.angle(volume)

    return {'result': True}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    module.disconnect()
