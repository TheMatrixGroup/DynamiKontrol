import threading
import serial
import time

# socat -d -d pty,link=tty_dk_rec,raw,echo=0 pty,link=tty_dk_sen,raw,echo=0

connected = False
port = 'tty_dk_rec'
baud = 9600

ser = serial.Serial(port, baud, timeout=0)

def handle_data(data):
    if data:
        print(data)

def read_from_port(ser):
    global connected
    while not connected:
        connected = True

        while True:
           reading = ser.readline().decode()
           handle_data(reading)
           time.sleep(0.01)

thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()