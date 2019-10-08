#!/usr/bin/env python3
import threading
import rospkg
import rospy
import random

import soundfx as soundfx

from tactics_ros.msg import tactic_comms 



def callback(data):
    rospy.loginfo("Choice is : %d" % (data.final_choice))
    if data.final_choice == "Shoot":
        shoot()

def shoot_sound():
    sounds = ["kachow.wav", "pew_pew.wav", "bang_bang.wav"]

    sound = soundfx.SoundFx(random.choice(sounds))
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
    rospy.Subscriber("tactics_chatter", tactics_comms, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass

