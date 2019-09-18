#!/user/bin/env python
import serial
port = "/dev/ttyACM0"

s1 = serial.Serial(port, 9600)
# s1.baudrate=9600

while True:
    read_ser = s1.read()
    read_ser = read_ser.decode("ascii")
    # print(read_ser)

if read_ser == 'A':
    print("Speed 1")

if read_ser == 'B':
    print("Speed 2")

if read_ser == 'H':
    print("Iv'e been hit")
