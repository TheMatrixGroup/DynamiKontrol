import time
import math
import warnings

class Servo(object):
    """Servo(Angle) motor submodule class.

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

            def cb(string):
                print(string)

            module.motor.angle(-45, func=cb, args=('hello',)) # print 'hello' when motor stopped at -45 degree.
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
            'angle_seq': 0x40,
            'angle_period_seq': 0x41,
            'get_offset': 0x81
        }


    def angle(self, angle, period=None, func=None, args=(), kwargs={}):
        """Control the angle of motor.

        Args:
            angle (int): If ``angle > 0`` moves along clockwise, otherwise moves along counter clockwise. ``angle`` must be between ``-85`` to ``85`` in degrees.
            period (float, optional): Control period. ``period`` must be between ``0.0`` to ``65.0`` in second. Defaults to ``None``.
            func (function, optional): Callback function when motor has been stopped. Defaults to ``None``.
            args (tuple, optional): args for callback function. Defaults to ``()``.
            kwargs (dict, optional): kwargs for callback function. Defaults to ``{}``.
        """
        direction = 0x00 if angle >= 0 else 0x01
        angle_hex = abs(angle)

        if func is None:
            if period is None:
                data = self.m.p2m.set_type(self.type).set_command(self.command['angle']).set_data([direction, angle_hex]).encode()
            else:
                if period < 0 or period > 65:
                    raise ValueError('Motor period value must be between 0.0 to 65.0 in second.')

                period = int(period * 1000)

                period_h = (period >> 8) & 0xff
                period_l = period & 0xff

                data = self.m.p2m.set_type(self.type).set_command(self.command['angle_period']).set_data([direction, angle_hex, period_h, period_l]).encode()
        else:
            if period is None:
                data = self.m.p2m.set_type(self.type).set_command(self.command['angle_seq']).set_data([direction, angle_hex, 0x00, 0x00, 0x00, 0x00, 0x00]).encode()
            else:
                if period < 0 or period > 65:
                    raise ValueError('Motor period value must be between 0.0 to 65.0 in second.')

                period = int(period * 1000)

                period_h = (period >> 8) & 0xff
                period_l = period & 0xff

                data = self.m.p2m.set_type(self.type).set_command(self.command['angle_period_seq']).set_data([direction, angle_hex, period_h, period_l, 0x00, 0x00, 0x00, 0x00, 0x00]).encode()

            self.m._add_motor_cb_func(func, args, kwargs)

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


class BLDC(object):
    """BLDC(Speed) motor submodule class.

    .. highlight:: python
    .. code-block:: python

        from dynamikontrol import Module
        import time

        module = Module()

        module.motor.speed(1000)
        time.sleep(5)
        module.motor.stop()

        module.disconnect()

    Args:
        module (object): Module object.
    """
    def __init__(self, module):
        self.m = module

        self.type = 0x04
        self.command = {
            'speed': 0x00,
            'speed_period': 0x01,
            'stop': 0x10,
            'speed_seq': 0x40,
            'speed_period_seq': 0x41,
            'get_speed': 0x81
        }


    def speed(self, speed, period=None, unit='rpm', func=None, args=(), kwargs={}):
        """Control speed of the motor.

        Args:
            speed (int): If ``speed > 0`` spins along clockwise, otherwise spins along counter clockwise.
            period (int, optional): Control period. ``period`` must be between ``0.0`` to ``65.0`` in second. Defaults to ``None``.
            unit (str, optional): Speed unit must be one of ``rpm``, ``deg/s`` and ``rad/s``. Defaults to ``'rpm'``.
            func (function, optional): Callback function when motor has been stopped. Defaults to ``None``.
            args (tuple, optional): args for callback function. Defaults to ``()``.
            kwargs (dict, optional): kwargs for callback function. Defaults to ``{}``.
        """
        direction = 0x00 if speed >= 0 else 0x01
        speed = abs(speed)

        unit = unit.lower()
        # 60 rpm == 360 deg/s == 360 * math.pi / 180 rad/s
        # 1 rpm == 6 deg/s == math.pi / 30 rad/s
        if unit == 'rad/s':
            speed = speed / (math.pi / 30)
        elif unit == 'deg/s':
            speed = speed / 6
        elif unit == 'rpm':
            pass
        else:
            raise ValueError('Motor unit value must be one of rpm, deg/s and rad/s.')

        speed = int(speed)

        if speed < 50:
            warnings.warn('Motor is not working properly when speed is less than 50 RPM.')

        if speed > 65535:
            raise ValueError('Motor speed value must be between 0 to 65535 in RPM.')

        speed_h = (speed >> 8) & 0xff
        speed_l = speed & 0xff

        if func is None:
            if period is None:
                data = self.m.p2m.set_type(self.type).set_command(self.command['speed']).set_data([direction, speed_h, speed_l]).encode()
            else:
                if period < 0 or period > 65:
                    raise ValueError('Motor period value must be between 0.0 to 65.0 in second.')

                period = int(period * 1000)

                period_h = (period >> 8) & 0xff
                period_l = period & 0xff

                data = self.m.p2m.set_type(self.type).set_command(self.command['speed_period']).set_data([direction, speed_h, speed_l, period_h, period_l]).encode()
        else:
            if period is None:
                data = self.m.p2m.set_type(self.type).set_command(self.command['speed_seq']).set_data([direction, speed_h, speed_l, 0x00, 0x00, 0x00, 0x00, 0x00]).encode()
            else:
                if period < 0 or period > 65:
                    raise ValueError('Motor period value must be between 0.0 to 65.0 in second.')

                period = int(period * 1000)

                period_h = (period >> 8) & 0xff
                period_l = period & 0xff

                data = self.m.p2m.set_type(self.type).set_command(self.command['speed_period_seq']).set_data([direction, speed_h, speed_l, period_h, period_l, 0x00, 0x00, 0x00, 0x00, 0x00]).encode()

            self.m._add_motor_cb_func(func, args, kwargs)

        self.m.send(data)


    def stop(self):
        """Stop the motor immediately.
        """
        data = self.m.p2m.set_type(self.type).set_command(self.command['stop']).set_data([]).encode()

        self.m.send(data)


    def get_speed(self, func, unit='rpm'):
        """Get speed of the motor asynchronously.

        .. highlight:: python
        .. code-block:: python

            from dynamikontrol import Module
            import time

            module = Module()

            module.motor.speed(4000, period=10)

            def get_speed_cb(speed):
                print('Current Speed', speed)

            for i in range(60):
                time.sleep(0.5)
                module.motor.get_speed(func=get_speed_cb)

            module.disconnect()

        Args:
            func (function): Callback function when getting speed from the motor.
            unit (str, optional): Speed unit must be one of ``rpm``, ``deg/s`` and ``rad/s``. Defaults to ``'rpm'``.
        """
        data = self.m.p2m.set_type(self.type).set_command(self.command['get_speed']).set_data([]).encode()
        self.m.send(data)

        if unit not in ['rad/s', 'deg/s', 'rpm']:
            raise ValueError('Motor unit value must be one of rpm, deg/s and rad/s.')

        self.m._add_get_speed_cb_func(func=func, unit=unit)


class Motor(object):
    def __init__(self, module):
        self.m = module

        if self.m.pid == '0001':
            self.motor = Servo(module=self.m)
        elif self.m.pid == '0002':
            self.motor = BLDC(module=self.m)

    def angle(self, *args, **kwargs):
        if self.m.pid != '0001':
            raise TypeError('angle() function is supported for DynamiKontrol Angle model only.')
        self.motor.angle(*args, **kwargs)

    def get_offset(self, *args, **kwargs):
        if self.m.pid != '0001':
            raise TypeError('get_offset() function is supported for DynamiKontrol Angle model only.')
        return self.motor.get_offset(*args, **kwargs)

    def set_offset(self, *args, **kwargs):
        if self.m.pid != '0001':
            raise TypeError('set_offset() function is supported for DynamiKontrol Angle model only.')
        self.motor.set_offset(*args, **kwargs)

    def speed(self, *args, **kwargs):
        if self.m.pid != '0002':
            raise TypeError('speed() function is supported for DynamiKontrol Speed model only.')
        self.motor.speed(*args, **kwargs)

    def stop(self, *args, **kwargs):
        if self.m.pid != '0002':
            raise TypeError('speed() function is supported for DynamiKontrol Speed model only.')
        self.motor.stop(*args, **kwargs)

    def get_speed(self, *args, **kwargs):
        if self.m.pid != '0002':
            raise TypeError('speed() function is supported for DynamiKontrol Speed model only.')
        self.motor.get_speed(*args, **kwargs)
