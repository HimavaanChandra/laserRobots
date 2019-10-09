#!/usr/bin/env python3
import threading
import rospkg
import rospy
import random
import os
import time

import soundfx as soundfx

from tactics_ros.msg import tactics_comms 



def callback(data):
    rospy.loginfo("Choice is : %s" % (data.final_choice))
    if data.final_choice == "F":
        shoot()
        time.sleep(3)

def shoot_sound():
    sounds = ["kachow.wav", "pew_pew.wav", "bang_bang.wav", "gun.wav"]
    dir_path = os.path.dirname(os.path.realpath(__file__))

    sound = soundfx.SoundFx(dir_path + "/" + random.choice(sounds))
    sound.play()
    sound.wait()

def shoot():
    shoot_thread_name = "shoot_sound"
    thread = threading.Thread(target=shoot_sound)
    thread.setName(shoot_thread_name)
    thread.start()


def main():

    # spin() simply keeps python from exiting until this node is stopped
    
    rospy.init_node('sound_node', anonymous=True)
    rospy.Subscriber("robot_choice_t", tactics_comms, callback)
    rospy.Subscriber("robot_choice_l", tactics_comms, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass

