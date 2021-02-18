import threading
import serial

port = 'tty_dk_sen'
baud = 9600

ser = serial.Serial(port, baud, timeout=0)
ser.write('hello'.encode())
