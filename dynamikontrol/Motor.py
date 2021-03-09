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
            'angle_period': 0x01
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


class Motor(object):
    def __init__(self, module):
        self.m = module

        # TODO: if statement by m.pid
        self.motor = Servo(module=self.m)

    def angle(self, *args, **kwargs):
        self.motor.angle(*args, **kwargs)
