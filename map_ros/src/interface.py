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
        self.scale_factor = 1.4
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
        xThomas = (data.xThomas / self.scale_factor) * self.m_unit
        yThomas = (data.yThomas / self.scale_factor)  * self.m_unit
        xLightning = (data.xLightning / self.scale_factor)  * self.m_unit
        yLightning = (data.yLightning / self.scale_factor)  * self.m_unit

        self.test.set(0, [xThomas, yThomas])
        self.test.set(1, [xLightning, yLightning])

    def broadcast(self):
        data = json.loads(self.test.data(0))
        
        msg = map_comms()

        msg.can_shoot = data["can_shoot"]
        msg.line_of_sight_start = data["line_of_sight"][0]
        msg.line_of_sight_end = data["line_of_sight"][1]
        msg.distances = data["distances"]
        msg.xThomas = int(data["player_x"])
        msg.yThomas = int(data["player_y"])
        msg.xLightning = int(data["enemy_x"])
        msg.yLightning = int(data["enemy_y"])

        if not rospy.is_shutdown():
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
        # interface.broadcast(1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    break

        screen.fill((0, 0, 0))
        interface.test.debug_draw(screen)
        pygame.display.flip()
        clock.tick(60)
        interface.broadcast()
        # time.sleep(5)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()    
    pygame.quit()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass

