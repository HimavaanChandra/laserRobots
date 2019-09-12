# Import socket module
import socket
import json


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 3322

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    name = input("Enter your name: ")
    s.send(name.encode('utf-8'))

    # message you send to server
    while True:
        message = input("Enter message: ")

        # message sent to server
        # s.send(message.encode('utf-8'))
        _send(s, {"Message": "Hello"})

        # messaga received from server
        data = s.recv(1024)
        

        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :', str(data.decode('ascii')))
    # close the connection
    s.close()


def _send(s, data):
  try:
    serialized = json.dumps(data)
  except (TypeError, ValueError) as e:
    raise Exception('You can only send JSON-serializable data')
  # send the length of the serialized data first
  length = '%d\n' % len(serialized)
  s.send(length.encode('utf-8'))
  # send the serialized data
  s.sendall(serialized.encode('utf-8'))

if __name__ == '__main__':
    Main()
