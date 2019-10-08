#!/user/bin/env python
import serial
import re
port="/dev/ttyACM0"

s1=serial.Serial(port,9600)
s1.flushInput()

done = False

while not done:

    my_string = ""
    line_is_done = False

    while not line_is_done:
        read_ser=s1.read()
        read_ser=read_ser.decode("ascii")

        if read_ser == "\n":
            line_is_done = True
            continue

        my_string += read_ser

    index = my_string.find(':')
    command = my_string[0:index]
    value = my_string[index+1:len(my_string)]
    
    if command == "Angle":
        print(command)
        print(value)
    if command == "Health":
        print(command)
        print(value)
    if command == "Shoot":
        print(value)
    if command == "Hit":
        print(value)
        
    #if re.match('Angle:',my_string):
        #print("Angle Found")
    #if re.match('Health:',my_string):
        #print("Health Found")
