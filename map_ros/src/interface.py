#!/usr/bin/env python3
import numpy as np
import time as time
import os
import pygame as pygame
import json as json
import rospkg
import rospy
from vision_ros.msg import vision_comms
from map_ros.msg import map_comms

from simlayer import SimLayer
from config import SCALE


def load_grid(filename="filename"):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    grid_csv = np.loadtxt(dir_path + "/" + filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list
    

class Interface():
    def __init__(self, grid):
        self.grid = grid
        self.sim = SimLayer(self.grid)
        self.m_unit = 1
        self.test = self.sim.spawn_instance("Test")
        self.test.spawn_robots(0, 0, 0, 0)

        rospy.init_node('map_node', anonymous=True)
        self.pub = rospy.Publisher('map_chatter', map_comms, queue_size=10)
        self.r = rospy.Rate(10) #10hz

        # self.test.spawn_robots(0, 0, 300, 300)

    def listen(self):
        rospy.Subscriber("robot_positions", vision_comms, self._update_pos)

        # spin() simply keeps python from exiting until this node is stopped

    def _update_pos(self, data):
        self.callback(data)
        xThomas = data.xThomas * self.m_unit
        yThomas = data.yThomas * self.m_unit
        xLightning = data.xLightning * self.m_unit
        yLightning = data.yLightning * self.m_unit

        self.test.set(0, [xThomas, yThomas])
        self.test.set(1, [xLightning, yLightning])

    def broadcast(self, robot):
        data = json.loads(self.test.data(robot))
        
        msg = map_comms()

        msg.can_shoot = data["can_shoot"]
        msg.line_of_sight = data["line_of_sight"]
        msg.distances = data["distances"]
        msg.xThomas = data["xThomas"]
        msg.yThomas = data["yThomas"]
        msg.xLightning = data["xLightning"]
        msg.yLightning = data["yLightning"]

        while not rospy.is_shutdown():
            rospy.loginfo(msg)
            self.pub.publish(msg)
            self.r.sleep()

    def callback(self, data):
        rospy.loginfo("Thomas %d is : %d" % (data.xThomas, data.yThomas))
        rospy.loginfo("Lightning %d is : %d" % (data.xLightning, data.yLightning))

        print("Thomas %d is : %d" % (data.xThomas, data.yThomas))
        print("Lightning %d is : %d" % (data.xLightning, data.yLightning))
        


def main():

    grid = load_grid()
    screen = pygame.display.set_mode([len(grid[0]) * SCALE, len(grid) * SCALE])
    pygame.display.set_caption('MAP Sim')
    clock = pygame.time.Clock()



    interface = Interface(grid)
    interface.listen()
    done = False
    while not done:
        interface.broadcast(0)
        interface.broadcast(1)
        time.sleep(5)

        screen.fill((0, 0, 0))
        interface.test.debug_draw(screen)
        pygame.display.flip()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass

