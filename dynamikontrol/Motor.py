import time

class Servo(object):
    """Servo motor submodule class.

    .. highlight:: python
    .. code-block:: python

        from dynamikontrol import Module
        import time

        module = Module()

        module.motor.angle(0)
        time.sleep(2)

        while True:
            module.motor.angle(45)
            time.sleep(2)

            module.motor.angle(-45)
            time.sleep(2)

        module.disconnect()

    Args:
        module (object): Module object.
    """
    def __init__(self, module):
        self.m = module

        self.type = 0x03
        self.command = {
            'angle': 0x00,
            'angle_period': 0x01,
            'set_offset': 0x02,
            'get_offset': 0x81
        }


    def angle(self, angle, period=None):
        """Control the angle of motor.

        Args:
            angle (int): If ``angle > 0`` moves along clockwise, otherwise moves along counter clockwise. ``angle`` must be between ``-85`` to ``85`` in degrees.
            period (uint): Control period. ``period`` must be between ``0`` to ``65535`` in millisecond. Defaults to ``None``.
        """
        direction = 0x00 if angle >= 0 else 0x01
        angle_hex = abs(angle)

        if period is None:
            data = self.m.p2m.set_type(self.type).set_command(self.command['angle']).set_data([direction, angle_hex]).encode()
        else:
            if period < 0 or period > 65535:
                raise ValueError('Motor period value must be between 0 to 65535 in millisecond.')

            period_h = (period >> 8) & 0xff
            period_l = period & 0xff

            data = self.m.p2m.set_type(self.type).set_command(self.command['angle_period']).set_data([direction, angle_hex, period_h, period_l]).encode()
        self.m.send(data)


    def get_offset(self):
        """Get offset of the motor.

        Returns:
            float: Offset of the motor in degree.
        """
        data = self.m.p2m.set_type(self.type).set_command(self.command['get_offset']).set_data([]).encode()

        command, received_data = self.m._manual_send_receive(data, 3 + 6)

        direction = 1 if received_data[0] == 0 else -1
        angle_int = received_data[1]
        angle_point = received_data[2] / 10.

        return direction * (angle_int + angle_point)


    def set_offset(self, angle):
        """Set offset of the motor. If the motor angle is inclined slightly even angle set to 0, you can adjust offset of the motor manually.

        Args:
            angle (float): Offset of the motor in degree. e.g) 17.5
        """
        direction = 0x00 if angle >= 0 else 0x01
        angle_hex = abs(angle)
        angle_int = int(angle_hex)
        angle_point = int(round(angle_hex - angle_int, 1) * 10)

        data = self.m.p2m.set_type(self.type).set_command(self.command['set_offset']).set_data([direction, angle_int, angle_point]).encode()
        self.m.send(data)

        time.sleep(0.1)
        self.angle(0)
        time.sleep(0.1)


class Motor(object):
    def __init__(self, module):
        self.m = module

        # TODO: if statement by m.pid
        self.motor = Servo(module=self.m)

    def angle(self, *args, **kwargs):
        self.motor.angle(*args, **kwargs)

    def get_offset(self, *args, **kwargs):
        return self.motor.get_offset(*args, **kwargs)

    def set_offset(self, *args, **kwargs):
        self.motor.set_offset(*args, **kwargs)
