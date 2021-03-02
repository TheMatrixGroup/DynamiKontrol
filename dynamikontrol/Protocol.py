class Protocol(object):
    header = 0x00
    command = 0x00
    data_length = 0x00
    data = bytearray()
    checksum = 0x00
    end = 0x04

    result = bytearray()

    def __init__(self):
        pass

    def encode_checksum(self):
        checksum = self.command ^ self.data_length
        for d in self.data:
            checksum ^= d
        return checksum

class PC2Module(Protocol):
    header = 0x05
    end = 0x04

    def __init__(self):
        super(PC2Module, self).__init__()

    def set_command(self, command):
        self.command = command
        return self

    def set_data(self, data):
        self.data = bytearray(data)
        self.data_length = len(self.data)
        return self

    def encode(self):
        self.result = bytearray()

        self.checksum = self.encode_checksum()

        self.result.append(self.header)
        self.result.append(self.command)
        self.result.append(self.data_length)
        self.result.extend(self.data)
        self.result.append(self.checksum)
        self.result.append(self.end)

        return self.result


class Module2PC(Protocol):
    end = 0x04

    def __init__(self):
        super(Module2PC, self).__init__()

    def decode(self, byte):
        try:
            byte = bytearray(byte)

            # TODO: Check header success or fail
            self.header = byte[0]
            self.command = byte[1]
            self.data_length = byte[2]
            self.data = byte[3:3+self.data_length]
            self.checksum = byte[-2]
            self.end = byte[-1]

            checksum = self.encode_checksum()

            if checksum != self.checksum:
                raise ValueError('Module2PC unmatched checksum')
        except:
            raise ValueError('Module2PC invalid protocol length')

        return self.command, self.data


if __name__ == '__main__':
    import time
    from Module import Module

    p2m = PC2Module()
    m2p = Module2PC()

    encoded = p2m.set_command(0x03).set_data([0x00, 0x01, 0x02]).encode() # status LED

    m = Module()
    m.send(encoded)

    m2p.decode(bytes(encoded)) # simulate response
    print(m2p.data)

    time.sleep(2)

    m.disconnect()
