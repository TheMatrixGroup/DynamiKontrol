class Servo(object):
    type = 0x03
    command = {
        'angle': 0x00
    }

    def __init__(self, module):
        self.m = module

    def angle(self, angle):
        direction = 0x00 if angle >= 0 else 0x01
        angle_hex = abs(angle)

        data = self.m.p2m.set_type(self.type).set_command(self.command['angle']).set_data([direction, angle_hex]).encode()
        self.m.send(data)

class Motor(object):
    def __init__(self, module):
        self.m = module

        # TODO: if statement by m.pid
        self.motor = Servo(module=self.m)

    def angle(self, *args, **kwargs):
        self.motor.angle(*args, **kwargs)
