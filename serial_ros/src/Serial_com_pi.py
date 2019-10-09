#!/usr/bin/env python3
import serial
import time

#ROS
import rospkg
import rospy
from serial_ros.msg import serial_comms
from tactics_ros.msg import tactics_comms_l
from tactics_ros.msg import tactics_comms_t
from astar_ros.msg import astar_comms



def send_to_ardunio(data):
    if hasattr(data, "final_choice"):
        command = data.final_choice
    elif hasattr(data, "path"):
        command = data.path
    else:
        rospy.logwarn("Command not recognised")
        return

    rospy.loginfo("Command: %s" % (command))
    s1.write(str(command + "\n").encode())
    time.sleep(2)

def read_serial():
    my_string = ""
    line_is_done = False

    while not line_is_done:
        read_ser=s1.read()
        read_ser=read_ser.decode("ascii")

        if read_ser == "\n":
            line_is_done = True
            continue

        my_string += read_ser

    return my_string

def read_from_ardunio():
    health = 0
    my_string = read_serial()

    index = my_string.find(':')
    command = my_string[0:index]
    value = my_string[index+1:len(my_string)]    

    if command == "Health":
        health=int(value)
        
    if not rospy.is_shutdown():
        msg = serial_comms()
        msg.health = health
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

rospy.init_node('serial_link_node', anonymous=True)
pub = rospy.Publisher('serial_link', serial_comms, queue_size=10)
rate = rospy.Rate(10)  #10hz

#Serial
port="/dev/ttyACM0"
s1=serial.Serial(port,9600)
s1.flushInput()

#Read from Arduino 
def main():
    done = False
    rospy.Subscriber("robot_choice_l", tactics_comms_l, send_to_ardunio)
    rospy.Subscriber("robot_choice_t", tactics_comms_t, send_to_ardunio)
    rospy.Subscriber("astar_path", astar_comms, send_to_ardunio)
    while not done:
        read_from_ardunio()
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass