#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk

import rospkg
import rospy
from vision_ros.msg import vision_comms
global temp 
temp = None

def callback(data):
    rospy.loginfo("Thomas %d is : %d" % (data.xThomas, data.yThomas))
    rospy.loginfo("Lightning %d is : %d" % (data.xLightning, data.yLightning))

    print("Thomas %d is : %d" % (data.xThomas, data.yThomas))
    print("Lightning %d is : %d" % (data.xLightning, data.yLightning))
    global temp
    temp = [data.xThomas, data.yThomas, data.xLightning, data.yLightning]
    print(temp)

# def main():
#     done = False
#     while not done:
rospy.init_node('scoreboard_listener_node', anonymous=True)
rospy.Subscriber("scoreboard_listener", vision_comms, callback)

        # spin() simply keeps python from exiting until this node is stopped
# rospy.spin()

# if __name__ == '__main__':
#     try:
#         main()
#     except rospy.ROSInterruptException: pass


root = Tk()
root.title("Scoreboard")

rootthomas = Tk()
rootthomas.title("Scoreboard")
mcqueenhp = 4
thomashp = 2

mcqueenhp1 = StringVar()
mcqueenhp2 = StringVar()
mcqueenhp3 = StringVar()
mcqueenhp4 = StringVar()
mcqueenhp5 = StringVar()

thomashp1 = StringVar(rootthomas)
thomashp2 = StringVar(rootthomas)
thomashp3 = StringVar(rootthomas)
thomashp4 = StringVar(rootthomas)
thomashp5 = StringVar(rootthomas)

if thomashp <= 5:
    thomashp1.set('O')
    thomashp2.set('O')
    thomashp3.set('O')
    thomashp4.set('O')
    thomashp5.set('O')

if thomashp<5: thomashp5.set('X')
if thomashp<4: thomashp4.set('X')
if thomashp<3: thomashp3.set('X')
if thomashp<2: thomashp2.set('X')
if thomashp<1: thomashp1.set('X')

if mcqueenhp <= 5:
    mcqueenhp1.set('O')
    mcqueenhp2.set('O')
    mcqueenhp3.set('O')
    mcqueenhp4.set('O')
    mcqueenhp5.set('O')

if mcqueenhp<5: mcqueenhp5.set('X')
if mcqueenhp<4: mcqueenhp4.set('X')
if mcqueenhp<3: mcqueenhp3.set('X')
if mcqueenhp<2: mcqueenhp2.set('X')
if mcqueenhp<1: mcqueenhp1.set('X')



mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe2 = ttk.Frame(rootthomas, padding="10")
mainframe2.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text='Lightning McQueen', width=25).grid(column=1, columnspan=5, row=1, sticky=(W))
ttk.Label(mainframe2, text='Thomas the Tank Engine', width=25).grid(column=1, columnspan=5, row=1, sticky=(E))

ttk.Label(mainframe, text='HEALTH', width=25).grid(column=1, columnspan=5, row=2, sticky=(W))
ttk.Label(mainframe2, text='HEALTH', width=25).grid(column=1, columnspan=5, row=2, sticky=(E))

ttk.Label(mainframe, textvariable=mcqueenhp1).grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp2).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp3).grid(column=3, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp4).grid(column=4, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp5).grid(column=5, row=3, sticky=(W, E))

ttk.Label(mainframe2, textvariable=thomashp1).grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp2).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp3).grid(column=3, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp4).grid(column=4, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp5).grid(column=5, row=3, sticky=(W, E))

mcqueenx = StringVar()
mcqueeny = StringVar()
thomasx = StringVar(rootthomas)
thomasy = StringVar(rootthomas)
if temp is not None:
    mcqueenx.set(temp[0])
    mcqueeny.set(temp[1])
    thomasx.set(temp[2])
    thomasy.set(temp[3])
else:
    mcqueenx.set(None)
    mcqueeny.set(None)
    thomasx.set(None)
    thomasy.set(None)

ttk.Label(mainframe, text='LOCATION', width=25).grid(column=1, columnspan=5, row=4, sticky=(W))
ttk.Label(mainframe2, text='LOCATION', width=25).grid(column=1, columnspan=5, row=4, sticky=(E))

ttk.Label(mainframe, text='x=').grid(column=1, row=5)
ttk.Label(mainframe, textvariable=mcqueenx).grid(column=2, columnspan=2, row=5)
ttk.Label(mainframe, text='y=').grid(column=4, row=5)
ttk.Label(mainframe, textvariable=mcqueeny).grid(column=5, columnspan=2, row=5)
ttk.Label(mainframe2, text='x=').grid(column=1, row=5)
ttk.Label(mainframe2, textvariable=thomasx).grid(column=2, columnspan=2, row=5)
ttk.Label(mainframe2, text='y=').grid(column=4, row=5)
ttk.Label(mainframe2, textvariable=thomasy).grid(column=5, columnspan=2, row=5)

# if mcqueenHasShot = 1:
#     ttk.Label(mainframe, text='Shots Fired', width=25).grid(column=1, columnspan=5, row=6)
# if thomasHasShot = 1:
#     ttk.Label(mainframe2, text='Shots Fired', width=25).grid(column=1, columnspan=5, row=6)

def test(*args):
    print("sucessfull test")
ttk.Button(mainframe, text='test', command=test).grid(column=3, row=1))
root.mainloop()
rootthomas.mainloop()

