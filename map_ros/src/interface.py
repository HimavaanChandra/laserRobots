#!/usr/bin/env python3
import numpy as np
import pygame as pygame
import rospkg
import rospy
from vision_ros.msg import vision_comms
from map_ros.msg import msg_comms

from .simlayer import SimLayer
from .config import SCALE


def load_grid(filename="filename"):
    grid_csv = np.loadtxt(filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list

def callback(data):
    rospy.loginfo("Thomas %d is : %d" % (data.xThomas, data.yThomas))
    rospy.loginfo("Lightning %d is : %d" % (data.xLightning, data.yLightning))

    print("Thomas %d is : %d" % (data.xThomas, data.yThomas))
    print("Lightning %d is : %d" % (data.xLightning, data.yLightning))

def main():
    done = False
    while not done:
        rospy.init_node('map_listener', anonymous=True)
        rospy.Subscriber("map_chatter", vision_comms, callback)

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

    grid = load_grid()

    sim = SimLayer(grid)

    test = sim.spawn_instance("Test " + str(i))
    test.spawn_robots(0, 0, 300, 300)

    done = False
    m_unit = 1
    while not done:
        test.move(robot, [int(x) * m_unit, int(y) * m_unit]


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
