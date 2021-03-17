# IoT Door Lock

You can build IoT smart door lock system that can be integrated in the mobile app and the web app.

In this example, we use Flask web framework.
You can also use Node.js and other languages and frameworks.

![](_static/iot_door_lock.gif)

## Source Code

Server `door_lock.py`

```python
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
```

Client `templates/index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>IoT Door Lock System</title>
  </head>

  <body>
    <div class="d-flex justify-content-center mt-5">
      <h5>IoT Door Lock System</h5>
    </div>
    <div class="d-flex justify-content-center">
      <div class="custom-control custom-switch">
        <input type="checkbox" class="custom-control-input" id="lockSwitch">
        <label class="custom-control-label" for="lockSwitch">Lock the Door</label>
      </div>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

    <script>
      $(function() {
        $('#lockSwitch').change(function(e) {
          $.ajax({
            method: 'POST',
            url: '/change',
            data: { is_locked: this.checked }
          })
          .done(function(msg) {
            console.log(msg);
          });
        });
      })
    </script>
  </body>
</html>
```