import socket
import threading
import soundfx as soundfx
import random

# print_lock = threading.Lock()


class TCPServer():
    def __init__(self, host="localhost", port=3322):
        self.host = host
        self.port = port
        self.listening = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        print("socket binded to port", port)
        self.client_threads = []

    def listen(self):
        self.socket.listen(4)
        print("socket is listening")
        while self.listening:
            client, address = self.socket.accept()
            client.settimeout(60)
            print('Connected to :', address[0], ':', address[1])
            client_thread = self.ClientThread(client, address)
            thread_name = "connection_" + str(len(self.client_threads))
            client_thread.setName(thread_name)
            client_thread.start()
            self.client_threads.append(client_thread)

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()

    class ClientThread(threading.Thread):
        def __init__(self, client, address):
            threading.Thread.__init__(self)
            self.client = client
            self.address = address
            self.timeout = 600
            self.connected = True
            self.client_name = None

        def run(self):
            size = 1024
            while self.connected:
                self.recieve_data(size)

        def recieve_data(self, size):
            try:
                data = self.client.recv(size)
                data = data.decode("utf-8")
                if data:
                    if self.client_name is None:
                        self.client_name = data
                    else:
                        self.handle_data(data)
                else:
                    raise ClientDisconnected("Client disconnected")
            except ClientDisconnected as error:
                print("Excepetion for:",
                      self.address[0], ':', self.address[1], " error:", error)
                self.close()
                return False

        def handle_data(self, data):
            if data == 'shoot':
                self.shoot()
            elif data == 'health':
                self.health(10)
            elif data == 'speed':
                self.speed(5)
            # Set the response to echo back the recieved data
            response = data.encode('utf-8')
            self.client.send(response)

        def shoot_sound(self):
            sounds = ["kachow.wav", "pew_pew.wav", "bang_bang.wav"]

            sound = soundfx.SoundFx(random.choice(sounds))
            sound.play()
            sound.wait()

        def health(self, health):
            print(self.client_name, "health:", health)

        def shoot(self):
            print(self.client_name, "shooting")
            shoot_thread_name = self.getName() + "_sound"
            thread = threading.Thread(target=self.shoot_sound)
            thread.setName(shoot_thread_name)
            thread.start()

        def speed(self, speed):
            print(self.client_name, "speed:", speed)

        def close(self):
            self.client.close()
            self.connected = False

        def __del__(self):
            self.close()


class ClientDisconnected(Exception):
    pass


def Main():
    server = TCPServer("localhost", 3322)
    server.listen()


if __name__ == '__main__':
    Main()
