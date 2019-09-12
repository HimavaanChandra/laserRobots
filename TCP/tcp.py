"""Base reuseable TCP Client Server"""

import socket
import threading
import json 

class TCP():
    def __init__(self, sock=None, host="localhost", port="3322"):
        self.encoding = 'utf-8'

        if socket is not None:
            self.socket = sock
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
        
        self.connected = True
    
    def send(self, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError):
            raise Exception('You can only send JSON-serializable data')
        
        # send the length of the serialized data first
        length = '%d\n' % len(serialized)
        self.socket.send(length.encode(self.encoding))
        # send the serialized data
        self.socket.sendall(serialized.encode(self.encoding))

    def recieve(self):
        try:
            data = self.deserialise()
            if data:
                return data
            else:
                raise TCPDisconnected("TCP disconnected")
        except TCPDisconnected as error:
            print("Excepetion for: error:", error)
            self.close()
            return False

    def deserialise(self):
        # read the length of the data, letter by letter until we reach EOL
        length_str = ''
        char = self.socket.recv(1)
        while char != '\n':
            length_str += char
            char = self.socket.recv(1)
        total = int(length_str)
        # use a memoryview to receive the data chunk by chunk efficiently
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = self.socket.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
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
        self.tcp = TCP(host=host, port=port)

    def send(self, data):
        self.tcp.send(data)

    def recieve(self):
        data = self.tcp.recieve()
        return data

    def __del__(self):
        self.tcp.__del__()


class TCP_Server():
    def __init__(self, host, port, connection_limit):
        self.tcp = TCP(host=host, port=port)

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

            client_thread = TCP_Thread(client_tcp, address, parent=self)
            thread_name = "connection_" + str(self.connection_count)
            self.add_thread(client_thread, thread_name)

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
        for thread in self.conection_threads:
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
        self.client_name = None

    def run(self):
        while self.connected:
            self.recieve_data()

    def recieve_data(self):
        data = self.tcp.recieve()
        self.handle_data(data)

    def handle_data(self, data):
        print(data)

    def close(self):
        self.tcp.__del__()
        self.connected = False

    def __del__(self):
        self.close()

class TCPDisconnected(Exception):
    pass