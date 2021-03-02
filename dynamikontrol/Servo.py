class Servo(object):
    def __init__(self, module):
        self.m = module

    def angle(self, angle):
        direction = 0x00 if angle >= 0 else 0x01
        angle_hex = abs(angle)

        data = self.m.p2m.set_command(0x05).set_data([direction, angle_hex]).encode()
        self.m.send(data)