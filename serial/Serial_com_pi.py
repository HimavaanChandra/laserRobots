import serial
import time
port="/dev/ttyACM0"

s1=serial.Serial(port,9600)
s1.flushInput()

#3Send to Arduino
time.sleep(2)
s1.write("N\n".encode())
time.sleep(2)
s1.write("NE\n".encode())
time.sleep(2)
s1.write("E\n".encode())
time.sleep(2)
s1.write("SE\n".encode())
time.sleep(2)
s1.write("S\n".encode())
time.sleep(2)
s1.write("SW\n".encode())
time.sleep(2)
s1.write("W\n".encode())
time.sleep(2)
s1.write("NW\n".encode())
time.sleep(2)
s1.write("Shoot\n".encode())
time.sleep(2)
s1.write("Hit\n".encode())
time.sleep(2)
s1.write("Reset\n".encode())
time.sleep(2)
s1.write("s_angle\n".encode())
#s_angle=345
#s1.write(str(s_angle).encode())
#time.sleep(2)



#Read from Arduino 
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
