import serial
from serial.tools import list_ports

import threading
import time

from dynamikontrol.Protocol import Module2PC, PC2Module
from dynamikontrol.LED import LED
from dynamikontrol.helpers.helper import print_bytearray

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

    def __init__(self, serial_no=None, debug=False):
        self.serial_no = serial_no
        self.debug = debug
        self.p2m = PC2Module()
        self.m2p = Module2PC()

        ports = list_ports.comports(include_links=True)

        # TODO: filter dk port and assign to port
        for port in ports:
            if self.debug:
                for i, p in enumerate(port):
                    print('[*] port[%d] %s' % (i, p))

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

        self.LED = LED(module=self)


    def connect(self):
        if self.port is None:
            raise IOError('Module is not connected!')

        self.ser = serial.Serial(self.port, self.baud, timeout=0)

        if self.debug:
            print('[*] Connected to %s, baud rate: %d' % (self.port, self.baud))

        self.receive_thread = threading.Thread(target=self.receive, args=())
        self.receive_thread.start()

        self.send(self.p2m.set_command(0x00).encode()) # connect


    def disconnect(self):
        if self.debug:
            print('[*] Disconnecting...')
        self.__stop_thread = True
        time.sleep(1)
        self.ser.close()


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

                    if not self.__is_header_defined and (data == 0x06 or data == 0x15): # 0x06 ACK, 0x15 NACK
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

                    if self.debug:
                        print('[*] Recv %s' % (print_bytearray(self.data_queue),))
                except Exception as e:
                    print(e)

        self.is_connected = False
        self.__stop_thread = False


    def send(self, data):
        if self.ser is None:
            raise IOError('Serial is not connected!')

        if self.port is None:
            raise IOError('Module is not connected!')

        if type(data) == str:
            self.ser.write(data.encode())
        else:
            self.ser.write(data)

        if self.debug:
            print('[*] Sent %s' % (print_bytearray(data),))


if __name__ == '__main__':
    m = Module(debug=True)

    time.sleep(0.1)

    m.disconnect()
