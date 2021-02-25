import serial
from serial.tools import list_ports

import threading
import time

class Module(object):
    serial_no = None
    port = None
    ser = None
    baud = 9600
    vid = None
    pid = None
    # TODO: our vids and pids
    avail_vids = ['0403']
    avail_pids = ['6001']

    is_connected = False

    __serial_receive_delay = 0.01
    __stop_thread = False

    def __init__(self, serial_no=None):
        self.serial_no = serial_no

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


    def handle_data(self, data):
        print(data)


    def receive(self):
        while not self.is_connected:
            self.is_connected = True
            self.__stop_thread = False

            while not self.__stop_thread:
                data = self.ser.readline()
                if data:
                    self.handle_data(data)
                time.sleep(self.__serial_receive_delay)

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
    m = Module()

    m.send('Hello world!')

    time.sleep(5)

    m.disconnect()
