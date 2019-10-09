#!/usr/bin/env python
import rospkg
import rospy
from vision_ros.msg import vision_comms

def callback(data):
    rospy.loginfo("Thomas %d is : %d" % (data.xThomas, data.yThomas))
    rospy.loginfo("Lightning %d is : %d" % (data.xLightning, data.yLightning))
    print("Thomas the tank engine" %)
    print("Location; x = %d, y = %d" % (data.xThomas, data.yThomas))
    print("Lightning McQueen" %)
    print("Location; x = %d, y = %d" % (data.xLightning, data.yLightning))
    

def listener():
    rospy.init_node('map_mode', anonymous=True)
    rospy.Subscriber("robot_positions", vision_comms, self.callback)  
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()