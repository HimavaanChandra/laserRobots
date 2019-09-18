#!/user/bin/env python
import serial
import tcp


def SerialLink(s1, client):
    while True:
        read_ser = s1.read()
        read_ser = read_ser.decode("ascii")
        if read_ser is not None:
            #print(read_ser)
            break

    if read_ser == 'A':
        print("Speed 1")
        client.send({"speed": 1})

    if read_ser == 'B':
        print("Speed 2")
        client.send({"speed": 2})

    if read_ser == 'H':
        print("Iv'e been hit")
        client.send({"shoot": 1})


def Main():
    port = "/dev/ttyACM1"

    s1 = serial.Serial(port, 9600)
    # s1.baudrate=9600


    # local host IP '127.0.0.1'
    host = '192.168.43.233'


    # Define the port on which you want to connect
    port = 3322
    print("Attempting to connect")
    client = tcp.TCP_Client(host, port)
    print("Connected")
    client.send({"name": "Pi 1"})

    # message you send to server
    while client.tcp.connected:
        SerialLink(s1, client)        

    # close the connection
    client.close()


if __name__ == '__main__':
    print("Launch")
    Main()

