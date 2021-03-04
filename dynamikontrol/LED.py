class LED(object):
    """LED submodule class.

    Args:
        module (object): Module object.
    """
    def __init__(self, module):
        self.m = module

        self.type = 0x01
        self.command = {
            'r': 0x00,
            'y': 0x01,
            'g': 0x02
        }
        self.mode = {
            'off': 0x00,
            'on': 0x01,
            'toggle': 0x02,
            'blink': 0x03
        }


    def __send(self, color, mode, on_delay=0, off_delay=0):
        on_low_bit = on_delay & 0xFF
        on_high_bit = (on_delay >> 8) & 0xFF

        off_low_bit = off_delay & 0xFF
        off_high_bit = (off_delay >> 8) & 0xFF

        data = self.m.p2m.set_type(self.type).set_command(self.command[color]).set_data([self.mode[mode], on_high_bit, on_low_bit, off_high_bit, off_low_bit]).encode()
        self.m.send(data)


    def off(self, color='all'):
        """Turn off the LED light

        Args:
            color (str, optional): Color of the LED light. ``r``, ``y`` or ``g``. Defaults to ``all``.
        """
        if color in ['all', 'r']:
            self.__send('r', 'off')

        if color in ['all', 'y']:
            self.__send('y', 'off')

        if color in ['all', 'g']:
            self.__send('g', 'off')


    def on(self, color='all'):
        """Turn on the LED light.

        Args:
            color (str, optional): Color of the LED light. ``r``, ``y`` or ``g``. Defaults to ``all``.
        """
        if color in ['all', 'r']:
            self.__send('r', 'on')

        if color in ['all', 'y']:
            self.__send('y', 'on')

        if color in ['all', 'g']:
            self.__send('g', 'on')


    def toggle(self, color='all'):
        """Toggle the LED light. Turn off while the light on status and turn on while the light off.

        Args:
            color (str, optional): Color of the LED light. ``r``, ``y`` or ``g``. Defaults to ``all``.
        """
        if color in ['all', 'r']:
            self.__send('r', 'toggle')

        if color in ['all', 'y']:
            self.__send('y', 'toggle')

        if color in ['all', 'g']:
            self.__send('g', 'toggle')


    def blink(self, color='all', on_delay=256, off_delay=256):
        """Blink the LED light periodically.

        Args:
            color (str, optional): Color of the LED light. ``r``, ``y`` or ``g``. Defaults to ``all``.
            on_delay (int, optional): Turn on delay in milliseconds. Defaults to ``256``.
            off_delay (int, optional): Turn off delay in milliseconds. Defaults to ``256``.
        """
        if color in ['all', 'r']:
            self.__send('r', 'blink', on_delay, off_delay)

        if color in ['all', 'y']:
            self.__send('y', 'blink', on_delay, off_delay)

        if color in ['all', 'g']:
            self.__send('g', 'blink', on_delay, off_delay)
