class LED(object):
    type = 0x01
    command = {
        'r': 0x00,
        'y': 0x01,
        'g': 0x02
    }
    mode = {
        'off': 0x00,
        'on': 0x01,
        'toggle': 0x02,
        'blink': 0x03
    }

    def __init__(self, module):
        self.m = module


    def __send(self, color, mode, on_interval=0, off_interval=0):
        on_low_bit = on_interval & 0xFF
        on_high_bit = (on_interval >> 8) & 0xFF

        off_low_bit = off_interval & 0xFF
        off_high_bit = (off_interval >> 8) & 0xFF

        data = self.m.p2m.set_type(self.type).set_command(self.command[color]).set_data([self.mode[mode], on_high_bit, on_low_bit, off_high_bit, off_low_bit]).encode()
        self.m.send(data)


    def off(self, color='all'):
        if color in ['all', 'r']:
            self.__send('r', 'off')

        if color in ['all', 'y']:
            self.__send('y', 'off')

        if color in ['all', 'g']:
            self.__send('g', 'off')


    def on(self, color='all'):
        if color in ['all', 'r']:
            self.__send('r', 'on')

        if color in ['all', 'y']:
            self.__send('y', 'on')

        if color in ['all', 'g']:
            self.__send('g', 'on')


    def toggle(self, color='all'):
        if color in ['all', 'r']:
            self.__send('r', 'toggle')

        if color in ['all', 'y']:
            self.__send('y', 'toggle')

        if color in ['all', 'g']:
            self.__send('g', 'toggle')


    def blink(self, color='all', on_interval=256, off_interval=256):
        if color in ['all', 'r']:
            self.__send('r', 'blink', on_interval, off_interval)

        if color in ['all', 'y']:
            self.__send('y', 'blink', on_interval, off_interval)

        if color in ['all', 'g']:
            self.__send('g', 'blink', on_interval, off_interval)
