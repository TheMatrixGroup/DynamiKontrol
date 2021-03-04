import serial
from serial.tools import list_ports

import threading
import time
import datetime

from dynamikontrol.Protocol import Module2PC, PC2Module
from dynamikontrol.LED import LED
from dynamikontrol.Motor import Motor
from dynamikontrol.helpers.helper import print_bytearray

class Module(object):
    serial_no = None
    port = None
    ser = None
    baud = 115200
    vid = None
    pid = None
    avail_vids = ['3476']
    serial_no_len = 8
    id_len = 1
    time_len = 8
    manual_delay = 0.1

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

        for port in ports:
            if self.debug:
                for i, p in enumerate(port):
                    print('[*] port[%d] %s' % (i, p))

            desc = port[2].lower()
            if 'vid:pid' not in desc:
                continue

            start_idx = desc.find('vid:pid=')
            self.vid, self.pid = desc[start_idx+8:start_idx+8+9].split(':')

            if self.vid not in self.avail_vids:
                continue

            start_idx = desc.find('ser=')
            serial_no_str = desc[start_idx+4:start_idx+4+8]

            if self.serial_no is not None and self.serial_no != serial_no_str:
                continue

            self.port = port[0]
            break

        self.connect()

        self.led = LED(module=self)
        self.motor = Motor(module=self)


    def connect(self):
        if self.port is None:
            raise IOError('Module is not connected!')

        self.ser = serial.Serial(self.port, self.baud, timeout=0)

        if self.debug:
            print('[*] Connected to %s, baud rate: %d' % (self.port, self.baud))

        self.receive_thread = threading.Thread(target=self.receive, args=())
        self.receive_thread._event = threading.Event()
        self.receive_thread.start()
        self.receive_thread._event.set()

        self.send(self.p2m.set_type(0x00).set_command(0x00).set_data([]).encode()) # connect
        time.sleep(self.manual_delay)


    def disconnect(self):
        time.sleep(1)
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
                self.receive_thread._event.wait()
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
                    self.data_queue.append(self.read_delay()) # type
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

                    if self.debug:
                        print('[*] Recv %s' % (print_bytearray(self.data_queue),))
                except Exception as e:
                    print(e)
                finally:
                    self.__is_header_defined = False

        self.is_connected = False
        self.__stop_thread = False


    def manual_send_receive(self, send_data, receive_data_len):
        self.receive_thread._event.clear() # pause receive thread

        self.send(send_data)
        time.sleep(self.manual_delay)

        received_data = bytearray()

        for i in range(receive_data_len):
            received_data.append(self.read_delay())

        command, received_data = self.m2p.decode(received_data)

        self.receive_thread._event.set() # resume receive thread

        return command, received_data


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


    def get_serial_no(self):
        command, serial_no = self.manual_send_receive(
            self.p2m.set_type(0x00).set_command(0x80).set_data([]).encode(),
            self.serial_no_len + 6
        )
        return serial_no.decode('utf-8')


    def get_id(self):
        command, id = self.manual_send_receive(
            self.p2m.set_type(0x00).set_command(0x81).set_data([]).encode(),
            self.id_len + 6
        )
        return id[0]


    def get_time(self):
        command, device_time = self.manual_send_receive(
            self.p2m.set_type(0x00).set_command(0x82).set_data([]).encode(),
            self.time_len + 6
        )

        # TODO: get_time() year, month, day
        h, m, s, ms, _, _, _, _ = device_time

        now = datetime.datetime.now()

        return datetime.datetime(now.year, now.month, now.day, h, m, s, ms)
