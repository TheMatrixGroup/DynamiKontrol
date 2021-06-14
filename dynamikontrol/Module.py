import serial
from serial.tools import list_ports

import threading
import time
import datetime
import math

from dynamikontrol.Protocol import Module2PC, PC2Module
from dynamikontrol.LED import LED
from dynamikontrol.BaseLED import BaseLED
from dynamikontrol.Motor import Motor
from dynamikontrol.Switch import Switch
from dynamikontrol.helpers.helper import print_bytearray

class Module(object):
    """Module class.

    .. highlight:: python
    .. code-block:: python

        from dynamikontrol import Module

        module = Module(serial_no) # specify the module by serial number

        # Print module serial number
        print('Serial number: %s' % (module.get_serial_no(),)

        module.disconnect()

    Args:
        serial_no (str): Specify serial number of the module.
        debug (bool): print debug messages.
    """
    __serial_receive_delay = 0
    __receive_thread_delay = 0.001
    __stop_thread = False
    _thread_daemon = True

    # communication
    __is_header_defined = False
    __avail_headers = [0x06, 0x15, 0x16, 0x17] # 0x06 ACK, 0x15 NACK, 0x16 SEQ, 0x17 DC1

    def __init__(self, serial_no=None, debug=False):
        self.serial_no = serial_no
        if self.serial_no is not None:
            self.serial_no = self.serial_no.lower()
        self.debug = debug
        self.p2m = PC2Module()
        self.m2p = Module2PC()

        self.fw_type = 0
        self.fw_version = None

        self.port = None
        self.ser = None
        self.baud = 115200
        self.vid = None
        self.pid = None
        self.avail_vids = ['3476']
        self.avail_pids = ['0001', '0002'] # [Angle, Speed]
        self.serial_no_len = 8
        self.id_len = 1
        self.time_len = 8
        self.fw_version_len = 8
        self.manual_delay = 0.1
        self.data_queue = bytearray()

        self.__motor_cb_func = None
        self.__motor_cb_args = ()
        self.__motor_cb_kwargs = {}

        self.__switch_cb_funcs = [{
            # channel 0
            'on': {
                'func': None,
                'args': (),
                'kwargs': {}
            },
            'off': {
                'func': None,
                'args': (),
                'kwargs': {}
            }
        }, {
            # channel 1
            'on': {
                'func': None,
                'args': (),
                'kwargs': {}
            },
            'off': {
                'func': None,
                'args': (),
                'kwargs': {}
            }
        }]

        self.__get_speed_cb_func = None
        self.__get_speed_unit = None

        self.is_connected = False

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

            if self.vid not in self.avail_vids or self.pid not in self.avail_pids:
                continue

            start_idx = desc.find('ser=')
            serial_no_str = desc[start_idx+4:start_idx+4+self.serial_no_len]

            if self.serial_no is not None and self.serial_no != serial_no_str:
                continue

            self.serial_no = serial_no_str
            self.port = port[0]
            break

        self.connect()

        self.led = LED(module=self)
        self.base_led = BaseLED(module=self)
        self.motor = Motor(module=self)
        self.switch = Switch(module=self)


    def connect(self):
        """Connect to the module.
        """
        if self.port is None:
            raise IOError('Module is not connected!')

        self.ser = serial.Serial(self.port, self.baud, timeout=0, write_timeout=0)

        if self.debug:
            print('[*] Connected to %s, baud rate: %d' % (self.port, self.baud))

        self.get_fw_version()
        time.sleep(0.1)

        self.receive_thread = threading.Thread(target=self.__receive, args=())
        self.receive_thread._event = threading.Event()
        self.receive_thread.daemon = self._thread_daemon
        self.receive_thread.start()
        self.receive_thread._event.set()

        self.send(self.p2m.set_type(0x00).set_command(0x00).set_data([]).encode()) # connect
        time.sleep(self.manual_delay)


    def disconnect(self):
        """Close the connection of the module. Must include ``module.disconnect()`` at the end of the code so that module can close connection properly.
        """
        self.send(self.p2m.set_type(0x00).set_command(0x10).set_data([]).encode()) # disconnect
        time.sleep(1)
        if self.debug:
            print('[*] Disconnecting...')
        self.__stop_thread = True
        time.sleep(1)
        self.ser.close()


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        self.disconnect()


    def __read_delay(self, size=1):
        """Read the data from the module using serial communication.

        Args:
            size (int, optional): Length of bytes. Defaults to ``1``.

        Returns:
            int: Data from the module.
        """
        time.sleep(self.__serial_receive_delay)
        return int.from_bytes(self.ser.read(size), byteorder='little')


    def __receive(self):
        """Receive data from the module. It runs on single thread for waiting response from the module.
        """
        while not self.is_connected:
            self.is_connected = True
            self.__stop_thread = False

            while not self.__stop_thread:
                self.receive_thread._event.wait()

                time.sleep(self.__receive_thread_delay)

                try:
                    header = self.__read_delay()

                    if not header:
                        continue

                    if not self.__is_header_defined and header in self.__avail_headers:
                        self.__is_header_defined = True
                        self.data_queue = bytearray()

                    if not self.__is_header_defined:
                        continue

                    # data queue
                    self.data_queue.append(header) # header
                    self.data_queue.append(self.__read_delay()) # type
                    self.data_queue.append(self.__read_delay()) # command

                    # data_length
                    data_length = self.__read_delay()
                    self.data_queue.append(data_length)

                    # data
                    for i in range(data_length):
                        self.data_queue.append(self.__read_delay())

                    self.data_queue.append(self.__read_delay()) # checksum

                    # end
                    end = self.__read_delay()
                    self.data_queue.append(end)

                    if end != 0x04:
                        self.__is_header_defined = False

                        if self.debug:
                            print('[!] Recv %s' % (print_bytearray(self.data_queue),))

                        raise ValueError('Module invalid end byte')

                    command, data = self.m2p.decode(self.data_queue)

                    # callbacks
                    if header == 0x16 and self.__motor_cb_func is not None:
                        self.__motor_cb_func(*self.__motor_cb_args, **self.__motor_cb_kwargs)
                    # switch callback
                    elif header == 0x17:
                        switch_ch = data[0]
                        if data[1] == 0:
                            switch_signal = 'on'
                        elif data[1] == 1:
                            switch_signal = 'off'

                        if self.__switch_cb_funcs[switch_ch][switch_signal]['func'] is not None:
                            self.__switch_cb_funcs[switch_ch][switch_signal]['func'](
                                *self.__switch_cb_funcs[switch_ch][switch_signal]['args'],
                                **self.__switch_cb_funcs[switch_ch][switch_signal]['kwargs']
                            )
                    # get speed callback
                    elif header == 0x06 and self.data_queue[1] == 0x04 and self.data_queue[2] == 0x81:
                        direction = 1 if self.data_queue[4] == 0 else -1
                        speed = (self.data_queue[5] << 8) | self.data_queue[6]

                        # 60 rpm == 360 deg/s == 360 * math.pi / 180 rad/s
                        # 1 rpm == 6 deg/s == math.pi / 30 rad/s
                        if self.__get_speed_unit == 'rad/s':
                            speed = speed * (math.pi / 30)
                        elif self.__get_speed_unit == 'deg/s':
                            speed = speed * 6
                        elif self.__get_speed_unit == 'rpm':
                            pass
                        else:
                            raise ValueError('Motor unit value must be one of rpm, deg/s and rad/s.')

                        self.__get_speed_cb_func(int(direction * speed))

                    if self.debug:
                        print('[*] Recv %s' % (print_bytearray(self.data_queue),))
                except Exception as e:
                    print(e)
                finally:
                    self.__is_header_defined = False

        self.is_connected = False
        self.__stop_thread = False


    def _add_motor_cb_func(self, func, args=(), kwargs={}):
        self.__motor_cb_func = func
        self.__motor_cb_args = args
        self.__motor_cb_kwargs = kwargs


    def _add_get_speed_cb_func(self, func, unit):
        self.__get_speed_cb_func = func
        self.__get_speed_unit = unit


    def _add_switch_cb_func(self, func, args=(), kwargs={}, ch=0, onoff='on'):
        self.__switch_cb_funcs[ch][onoff]['func'] = func
        self.__switch_cb_funcs[ch][onoff]['args'] = args
        self.__switch_cb_funcs[ch][onoff]['kwargs'] = kwargs


    def _manual_send_receive(self, send_data, receive_data_len):
        """Pause receiving thread, send/receive data manually and resume receiving thread.

        Args:
            send_data (bytearray of int): Data to send.
            receive_data_len (int): Length of the data to receive.

        Returns:
            tuple: (command, received data)
        """
        if hasattr(self, 'receive_thread'):
            self.receive_thread._event.clear() # pause receive thread

        time.sleep(self.manual_delay)
        self.send(send_data)
        time.sleep(self.manual_delay)

        received_data = bytearray()

        for i in range(receive_data_len):
            received_data.append(self.__read_delay())

        if self.debug:
            print('[*] Recv %s' % (print_bytearray(received_data),))

        command, received_data = self.m2p.decode(received_data)

        if hasattr(self, 'receive_thread'):
            self.receive_thread._event.set() # resume receive thread

        return command, received_data


    def send(self, data):
        """Send the data to the module

        Args:
            data (bytearray of int): Data to send.
        """
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
        """Get serial number of the connected module.

        Returns:
            str: Serial number.
        """
        command, serial_no = self._manual_send_receive(
            self.p2m.set_type(0x00).set_command(0x80).set_data([]).encode(),
            self.serial_no_len + 6
        )
        return serial_no.decode('utf-8')


    def get_id(self):
        """Get ID of the connected module.

        Returns:
            int: Module ID.
        """
        command, id = self._manual_send_receive(
            self.p2m.set_type(0x00).set_command(0x81).set_data([]).encode(),
            self.id_len + 6
        )
        return id[0]


    def get_time(self):
        """Get device time of the connected module.

        Returns:
            datetime: Device time.
        """
        command, device_time = self._manual_send_receive(
            self.p2m.set_type(0x00).set_command(0x82).set_data([]).encode(),
            self.time_len + 6
        )

        # TODO: get_time() year, month, day
        h, m, s, ms, _, _, _, _ = device_time

        now = datetime.datetime.now()

        return datetime.datetime(now.year, now.month, now.day, h, m, s, ms)


    def get_fw_version(self):
        """Get firmware version of the connected module.

        Returns:
            str: Device firmware version.
        """
        command, fw_data = self._manual_send_receive(
            self.p2m.set_type(0x00).set_command(0x83).set_data([]).encode(),
            self.fw_version_len + 6
        )

        self.fw_type = fw_data[0]

        fw_major_version = int(fw_data[1:4].decode('utf-8'))
        fw_minor_version = fw_data[5:8].decode('utf-8')
        self.fw_version = '%s.%s' % (fw_major_version, fw_minor_version)

        return self.fw_version


    def set_default_switch_operation(self, on):
        """Set either turn default switch operation on or not. Motor is spinning when switch is pressed by default.

        Args:
            on (bool): Set default operation on or off.
        """

        onoff = 0x00
        if on:
            onoff = 0x01

        data = self.p2m.set_type(0x00).set_command(0x03).set_data([onoff]).encode()

        self.send(data)
