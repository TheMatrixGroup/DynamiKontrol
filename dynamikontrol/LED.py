class LED(object):
    def __init__(self, module):
        self.m = module

    # TODO: all led on
    def on(self, id):
        data = self.m.p2m.set_command(0x03).set_data([0x01, 0x01, 0x01]).encode()
        self.m.send(data)


    # TODO: all led off
    def off(self, id):
        data = self.m.p2m.set_command(0x03).set_data([0x00, 0x00, 0x00]).encode()
        self.m.send(data)

    # TODO: all led toggle
    def toggle(self, id):
        data = self.m.p2m.set_command(0x03).set_data([0x02, 0x02, 0x02]).encode()
        self.m.send(data)
