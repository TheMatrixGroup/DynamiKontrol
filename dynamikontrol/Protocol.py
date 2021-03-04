class Protocol(object):
    header = 0x00
    type = 0x00
    command = 0x00
    data_length = 0x00
    data = bytearray()
    checksum = 0x00
    end = 0x04

    result = bytearray()

    def __init__(self):
        pass

    def encode_checksum(self):
        checksum = self.type ^ self.command ^ self.data_length
        for d in self.data:
            checksum ^= d
        return checksum

class PC2Module(Protocol):
    header = 0x05
    end = 0x04

    def __init__(self):
        super(PC2Module, self).__init__()

    def set_type(self, type):
        self.type = type
        return self

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
        self.result.append(self.type)
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
            self.type = byte[1]
            self.command = byte[2]
            self.data_length = byte[3]
            self.data = byte[4:4+self.data_length]
            self.checksum = byte[-2]
            self.end = byte[-1]

            checksum = self.encode_checksum()

            if checksum != self.checksum:
                raise ValueError('Module2PC unmatched checksum')
        except:
            raise ValueError('Module2PC invalid protocol length')

        return self.command, self.data
