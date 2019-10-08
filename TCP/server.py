import threading
import soundfx as soundfx
import random
import datetime
import tcp


class ROS_TCP_Server(tcp.TCP_Server):
    def __init__(self, host, port, connection_limit):
        super().__init__(host, port, connection_limit)

    def create_thread(self, tcp, address, parent=None):
        return ROS_TCP_Thread(tcp, address, parent=parent)


class ROS_TCP_Thread(tcp.TCP_Thread):
    def __init__(self, tcp, address, parent=None):
        super().__init__(tcp, address, parent)
        self.robot = "unknown"

    def handle_data(self, data):
        if "name" in data:
            self.robot = data["name"]
        if "shoot" in data:
            self.shoot()
        if "health" in data:
            self.health(data["health"])
        if "speed" in data:
            self.speed(data["speed"])
        # Set the response to echo back the recieved data
        response = data
        self.tcp.send(response)

    def console_log(self, log):
        log = log.rjust(16, " ")
        robot = self.robot
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print("[{0:8}] : {1:20} {2}".format(timestamp, robot, log))

    def shoot_sound(self):
        sounds = ["kachow.wav", "bang_bang.wav"]

        sound = soundfx.SoundFx(random.choice(sounds))
        sound.play()
        sound.wait()

    def health(self, health):
        self.console_log("health: {0}".format(health))

    def shoot(self):

        self.console_log("shooting")
        shoot_thread_name = self.getName() + "_sound"
        thread = threading.Thread(target=self.shoot_sound)
        thread.setName(shoot_thread_name)
        thread.start()

    def speed(self, speed):
        self.console_log("speed: {0}".format(speed))


def Main():

    server = ROS_TCP_Server("0.0.0.0", 3322, 3)
    server.listen()

    # server = TCPServer("localhost", 3322)
    # server.listen()


if __name__ == '__main__':
    Main()
