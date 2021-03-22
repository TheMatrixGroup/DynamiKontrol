class BaseLED(object):
    def __init__(self, module):
        self.m = module

        self.type = 0x02
        self.command = {
            'r': 0x00,
            'g': 0x01,
            'b': 0x02,
            'mix': 0x03,
        }
        self.mode = {
            'off': 0x00,
            'on': 0x01,
            'toggle': 0x02,
        }

        self.mix_on_time = 10 # ms


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
            color (str, optional): Color of the LED light. ``r``, ``g`` or ``b``. Defaults to ``all``.
        """
        if color in ['all', 'r']:
            self.__send('r', 'off')

        if color in ['all', 'g']:
            self.__send('g', 'off')

        if color in ['all', 'b']:
            self.__send('b', 'off')


    def on(self, color='all'):
        """Turn on the LED light.
        Args:
            color (str, optional): Color of the LED light. ``r``, ``g`` or ``b``. Defaults to ``all``.
        """
        if color in ['all', 'r']:
            self.__send('r', 'on')

        if color in ['all', 'g']:
            self.__send('g', 'on')

        if color in ['all', 'b']:
            self.__send('b', 'on')


    def toggle(self, color='all'):
        """Toggle the LED light. Turn off while the light on status and turn on while the light off.
        Args:
            color (str, optional): Color of the LED light. ``r``, ``g`` or ``b``. Defaults to ``all``.
        """
        if color in ['all', 'r']:
            self.__send('r', 'toggle')

        if color in ['all', 'g']:
            self.__send('g', 'toggle')

        if color in ['all', 'b']:
            self.__send('b', 'toggle')


    def mix(self, rgb):
        """Mix the color of base LED light.

        Args:
            rgb ([tuple]): Intensity of LED lights. Range from 0 to 100. e.g) (100, 0, 0) red light
        """
        r, g, b = rgb

        on_low_bit = self.mix_on_time & 0xFF
        on_high_bit = (self.mix_on_time >> 8) & 0xFF

        data = self.m.p2m.set_type(self.type).set_command(self.command['mix']).set_data([on_high_bit, on_low_bit, r, g, b]).encode()
        self.m.send(data)
