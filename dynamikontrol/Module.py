import serial
from serial.tools import list_ports

import threading
import time

class Module(object):
    port = None
    ser = None
    baud = 9600
    vid = None
    pid = None
    is_connected = False

    serial_receive_delay = 0.01
    __stop_thread = False

    def __init__(self, serial_no=None):
        ports = list_ports.comports(include_links=True)

        # TODO: filter dk port and assign to port
        # TODO: filter by vid, pid
        for port in ports:
            desc = port[2].lower()
            if 'vid:pid' not in desc:
                continue

            start_idx = desc.find('vid:pid=')
            self.vid, self.pid = port[2][start_idx+8:start_idx+8+9].split(':')

        # TODO: delete hard code
        self.port = 'tty_dk_rec'

        self.connect()


    def connect(self):
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
                data = self.ser.readline().decode()
                if data:
                    self.handle_data(data)
                time.sleep(self.serial_receive_delay)

        self.is_connected = False
        self.__stop_thread = False
        self.ser = None


    def send(self, data):
        if self.ser is None:
            raise IOError('Serial is not connected!')

        # TODO: remove test serial port
        ser = serial.Serial('tty_dk_sen', self.baud, timeout=0)
        ser.write(data.encode())


if __name__ == '__main__':
    m = Module()

    print(m.__stop_thread)
    m.send('Hello world!')

    time.sleep(5)

    m.disconnect()
