import serial
from serial.tools import list_ports

import threading
import time

from Protocol import Module2PC

class Module(object):
    serial_no = None
    port = None
    ser = None
    baud = 115200
    vid = None
    pid = None
    # TODO: our vids and pids
    avail_vids = ['0403', '03eb']
    avail_pids = ['6001', '2044']

    is_connected = False

    __serial_receive_delay = 0
    __stop_thread = False

    # communication
    __is_header_defined = False
    data_queue = bytearray()

    def __init__(self, serial_no=None):
        self.serial_no = serial_no
        self.m2p = Module2PC()

        ports = list_ports.comports(include_links=True)

        # TODO: filter dk port and assign to port
        for port in ports:
            desc = port[2].lower()
            if 'vid:pid' not in desc:
                continue

            start_idx = desc.find('vid:pid=')
            self.vid, self.pid = desc[start_idx+8:start_idx+8+9].split(':')

            if self.vid not in self.avail_vids or self.pid not in self.avail_pids:
                continue

            start_idx = desc.find('ser=')
            serial_no_str = desc[start_idx+4:start_idx+4+8]

            if self.serial_no is not None and self.serial_no != serial_no_str:
                continue

            self.port = port[0]
            break

        self.connect()


    def connect(self):
        if self.port is None:
            raise IOError('Module is not connected!')

        self.ser = serial.Serial(self.port, self.baud, timeout=0)

        self.receive_thread = threading.Thread(target=self.receive, args=())
        self.receive_thread.start()


    def disconnect(self):
        self.__stop_thread = True
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.close()
        time.sleep(2)


    def read_delay(self, size=1):
        time.sleep(self.__serial_receive_delay)
        return int.from_bytes(self.ser.read(size), byteorder='little')


    def receive(self):
        while not self.is_connected:
            self.is_connected = True
            self.__stop_thread = False

            while not self.__stop_thread:
                try:
                    data = self.read_delay()

                    if not data:
                        continue

                    # TODO: check header field, remove 0x05
                    if not self.__is_header_defined and (data == 0x05 or data == 0x06 or data == 0x15): # 0x06 ACK, 0x15 NACK
                        self.__is_header_defined = True
                        self.data_queue = bytearray()

                    if not self.__is_header_defined:
                        continue

                    # data queue
                    self.data_queue.append(data) # header
                    self.data_queue.append(self.read_delay()) # command

                    # data_length
                    data_length = self.read_delay()
                    self.data_queue.append(data_length)

                    # data
                    for i in range(data_length):
                        self.data_queue.append(self.read_delay())

                    self.data_queue.append(self.read_delay()) # checksum

                    # end
                    end = self.read_delay()
                    self.data_queue.append(end)

                    if end != 0x04:
                        self.__is_header_defined = False
                        raise ValueError('Module invalid end byte')

                    data = self.m2p.decode(self.data_queue)

                    self.__is_header_defined = False
                except Exception as e:
                    print(e)

        self.is_connected = False
        self.__stop_thread = False
        self.ser = None


    def send(self, data):
        if self.ser is None:
            raise IOError('Serial is not connected!')

        if self.port is None:
            raise IOError('Module is not connected!')

        if type(data) == str:
            self.ser.write(data.encode())
        else:
            self.ser.write(data)


if __name__ == '__main__':
    from Protocol import PC2Module

    p2m = PC2Module()

    encoded = p2m.set_command(0x00).encode()
    print('send', encoded)

    m = Module()
    m.send(encoded)
    
    print('received command', m.m2p.command, m.m2p.data)
    print('received data', m.m2p.data)

    time.sleep(0.1)

    m.disconnect()
