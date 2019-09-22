"""Base reuseable TCP Client Server"""

import socket
import threading
import json


class TCP():
    def __init__(self, sock=None):
        self.encoding = 'utf-8'
        self.socket = sock
        if self.socket is not None:
            self.connected = True
        else:
            self.connected = False

    def server(self, host="localhost", port="3322"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.connected = True

    def client(self, host="localhost", port="3322"):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
        except ConnectionRefusedError:
            print("Target host unreachable: {0}:{1}".format(host, port))
            self.close()

    def send(self, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError):
            raise Exception('You can only send JSON-serializable data')

        try:
            if self.connected is False:
                raise TCPDisconnected("TCP disconnected")

            # send the length of the serialized data first
            length = '%d\n' % len(serialized)
            self.socket.send(length.encode(self.encoding))
            # send the serialized data
            self.socket.sendall(serialized.encode(self.encoding))
            return True

        except (TCPDisconnected, ConnectionAbortedError, ConnectionResetError) as error:
            print("Excepetion for recieving data, error:", error)
            self.close()
            return False

    def receive(self):
        try:
            if self.connected is False:
                raise TCPDisconnected("TCP disconnected")

            data = self.deserialise()
            if data:
                return data
            else:
                raise TCPDisconnected("No data recieved")

        except TCPTimeout as error:
            print("Socket Timeout: ", error)
            return False

        except (ConnectionResetError, TCPDisconnected) as error:
            print("Excepetion for recieving data, error:", error)
            self.close()
            return False

    def deserialise(self):
        """Recieve data and convert in to json"""
        def data_length():
            # read the length of the data, letter by letter until we reach EOL
            length_str = ''
            char = self.socket.recv(1).decode(self.encoding)
            while char != '\n':
                length_str += char
                char = self.socket.recv(1).decode(self.encoding)
            return int(length_str)

        def recieve_data(data_length):
            # use a memoryview to receive the data chunk by chunk efficiently
            view = memoryview(bytearray(data_length))
            next_offset = 0
            while data_length - next_offset > 0:
                recv_size = self.socket.recv_into(
                    view[next_offset:],
                    data_length - next_offset)

                next_offset += recv_size
            return view

        data_length = data_length()
        view = recieve_data(data_length)

        try:
            deserialized = json.loads(view.tobytes())
        except (TypeError, ValueError):
            raise Exception('Data received was not in JSON format')
        return deserialized

    def close(self):
        self.socket.close()
        self.connected = False

    def __del__(self):
        self.close()


class TCP_Client():
    def __init__(self, host, port):
        self.tcp = TCP()
        self.tcp.client(host=host, port=port)

    def send(self, data):
        self.tcp.send(data)

    def receive(self):
        data = self.tcp.receive()
        return data

    def close(self):
        self.tcp.__del__()

    def __del__(self):
        self.close()


class TCP_Server():
    def __init__(self, host, port, connection_limit=4):
        self.tcp = TCP()
        self.tcp.server(host=host, port=port)

        self.listening = True
        self.connection_threads = []
        self.connection_count = 0
        self.connection_limit = connection_limit
        self.timeout_limit = 600

    def listen(self):
        self.tcp.socket.listen(self.connection_limit)
        print("socket is listening")
        while self.listening:
            client_socket, address = self.tcp.socket.accept()
            client_socket.settimeout(self.timeout_limit)

            client_tcp = TCP(sock=client_socket)
            print('Connected to :', address[0], ':', address[1])

            client_thread = self.create_thread(
                client_tcp, address, parent=self)
            thread_name = "connection_" + str(self.connection_count)
            self.add_thread(client_thread, thread_name)

    def create_thread(self, tcp, address, parent=None):
        return TCP_Thread(tcp, address, parent=parent)

    def add_thread(self, thread, name):
        thread.setName(name)
        thread.start()

        self.connection_threads.append(thread)
        self.connection_count += 1

    def remove_thread(self, thread):
        thread.close()
        thread.join()
        # self.connection_threads.del()

    def __del__(self):
        for thread in self.connection_threads:
            self.remove_thread(thread)
        # self.conection_threads.clear()
        self.tcp.__del__()


class TCP_Thread(threading.Thread):
    def __init__(self, tcp, address, parent=None):
        threading.Thread.__init__(self)
        self.tcp = tcp
        self.parent = parent

        self.address = address
        self.timeout = 600
        self.connected = True

    def run(self):
        while self.connected and self.tcp.connected:
            self.receive_data()

    def receive_data(self):
        data = self.tcp.receive()
        if data is not False:
            self.handle_data(data)
        else:
            self.close()

    def handle_data(self, data):
        print(data)
        self.tcp.send(data)

    def close(self):
        self.tcp.__del__()
        self.connected = False

    def __del__(self):
        self.close()


class TCPDisconnected(Exception):
    pass


class TCPTimeout(socket.timeout):
    pass
