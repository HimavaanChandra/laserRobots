"""Client"""
import tcp


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 3322

    client = tcp.TCP_Client(host, port)

    # message you send to server
    while client.tcp.connected:
        command = input("Enter command: ")
        value = input("Enter value: ")
        client.send({command: value})

        try:
            data = client.receive()
            print('Received from the server :')
            print(data)
        except tcp.TCPTimeout:
            print('Socket Timeout, awaiting new commands')

    # close the connection
    client.close()


if __name__ == '__main__':
    Main()
