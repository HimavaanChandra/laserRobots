#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk

import rospkg
import rospy
from vision_ros.msg import vision_comms
from serial_ros.msg import serial_comms
global temp 
temp = None

def callback(data):
    rospy.loginfo("Thomas is at %d : %d, and %d" % (data.xThomas, data.yThomas, data.health))
    rospy.loginfo("Lightning is at %d : %d, and %d" % (data.xLightning, data.yLightning))

    global temp
    temp = [data.xThomas, data.yThomas, data.xLightning, data.yLightning, data.health]
    print(temp)
    root.after(200, function)

rospy.init_node('scoreboard', anonymous=True)
rospy.Subscriber("robot_positions", vision_comms, callback)
rospy.Subscriber("serial_link", serial_comms, callback)


root = Tk()
root.title("Scoreboard")

rootthomas = Tk()
rootthomas.title("Scoreboard")

mcqueenhp1 = StringVar()
mcqueenhp2 = StringVar()
mcqueenhp3 = StringVar()
mcqueenhp4 = StringVar()
mcqueenhp5 = StringVar()
mcqueenhp6 = StringVar()
mcqueenhp7 = StringVar()
mcqueenhp8 = StringVar()
mcqueenhp9 = StringVar()
mcqueenhp10 = StringVar()

thomashp1 = StringVar(rootthomas)
thomashp2 = StringVar(rootthomas)
thomashp3 = StringVar(rootthomas)
thomashp4 = StringVar(rootthomas)
thomashp5 = StringVar(rootthomas)
thomashp6 = StringVar(rootthomas)
thomashp7 = StringVar(rootthomas)
thomashp8 = StringVar(rootthomas)
thomashp9 = StringVar(rootthomas)
thomashp10 = StringVar(rootthomas)


mcqueenx = StringVar()
mcqueeny = StringVar()
thomasx = StringVar(rootthomas)
thomasy = StringVar(rootthomas)

def function():
    if temp is not None:
        mcqueenx.set(temp[0])
        mcqueeny.set(temp[1])
        thomasx.set(temp[2])
        thomasy.set(temp[3])
        mcqueenhp = temp[4]
        thomashp = temp[5]
    else:
        mcqueenx.set(None)
        mcqueeny.set(None)
        thomasx.set(None)
        thomasy.set(None)
        mcqueenhp = 10
        thomashp = 10

    if thomashp <= 10:
        thomashp1.set('O')
        thomashp2.set('O')
        thomashp3.set('O')
        thomashp4.set('O')
        thomashp5.set('O')
        thomashp6.set('O')
        thomashp7.set('O')
        thomashp8.set('O')
        thomashp9.set('O')
        thomashp10.set('O')

    if thomashp<10: thomashp10.set('X')
    if thomashp<9: thomashp9.set('X')
    if thomashp<8: thomashp8.set('X')
    if thomashp<7: thomashp7.set('X')
    if thomashp<6: thomashp6.set('X')
    if thomashp<5: thomashp5.set('X')
    if thomashp<4: thomashp4.set('X')
    if thomashp<3: thomashp3.set('X')
    if thomashp<2: thomashp2.set('X')
    if thomashp<1: thomashp1.set('X')

    if mcqueenhp <= 10:
        mcqueenhp1.set('O')
        mcqueenhp2.set('O')
        mcqueenhp3.set('O')
        mcqueenhp4.set('O')
        mcqueenhp5.set('O')
        mcqueenhp6.set('O')
        mcqueenhp7.set('O')
        mcqueenhp8.set('O')
        mcqueenhp9.set('O')
        mcqueenhp10.set('O')

    if mcqueenhp<10: mcqueenhp5.set('X')
    if mcqueenhp<9: mcqueenhp4.set('X')
    if mcqueenhp<8: mcqueenhp3.set('X')
    if mcqueenhp<7: mcqueenhp2.set('X')
    if mcqueenhp<6: mcqueenhp1.set('X')
    if mcqueenhp<5: mcqueenhp5.set('X')
    if mcqueenhp<4: mcqueenhp4.set('X')
    if mcqueenhp<3: mcqueenhp3.set('X')
    if mcqueenhp<2: mcqueenhp2.set('X')
    if mcqueenhp<1: mcqueenhp1.set('X')

function()

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

ttk.Label(mainframe, textvariable=mcqueenhp1, width=3).grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp2, width=3).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp3, width=3).grid(column=3, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp4, width=3).grid(column=4, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp5, width=3).grid(column=5, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp6, width=3).grid(column=6, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp7, width=3).grid(column=7, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp8, width=3).grid(column=8, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp9, width=3).grid(column=9, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=mcqueenhp10, width=3).grid(column=10, row=3, sticky=(W, E))

ttk.Label(mainframe2, textvariable=thomashp1, width=3).grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp2, width=3).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp3, width=3).grid(column=3, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp4, width=3).grid(column=4, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp5, width=3).grid(column=5, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp6, width=3).grid(column=6, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp7, width=3).grid(column=7, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp8, width=3).grid(column=8, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp9, width=3).grid(column=9, row=3, sticky=(W, E))
ttk.Label(mainframe2, textvariable=thomashp10, width=3).grid(column=10, row=3, sticky=(W, E))

ttk.Label(mainframe, text='LOCATION', width=25).grid(column=1, columnspan=5, row=4, sticky=(W))
ttk.Label(mainframe2, text='LOCATION', width=25).grid(column=1, columnspan=5, row=4, sticky=(E))

ttk.Label(mainframe, text='x =').grid(column=1, row=5)
ttk.Label(mainframe, textvariable=mcqueenx).grid(column=2, columnspan=2, row=5)
ttk.Label(mainframe, text='y =').grid(column=4, row=5)
ttk.Label(mainframe, textvariable=mcqueeny).grid(column=5, columnspan=2, row=5)
ttk.Label(mainframe2, text='x =').grid(column=1, row=5)
ttk.Label(mainframe2, textvariable=thomasx).grid(column=2, columnspan=2, row=5)
ttk.Label(mainframe2, text='y =').grid(column=4, row=5)
ttk.Label(mainframe2, textvariable=thomasy).grid(column=5, columnspan=2, row=5)

# if mcqueenHasShot = 1:
#     ttk.Label(mainframe, text='Shots Fired', width=25).grid(column=1, columnspan=5, row=6)
# if thomasHasShot = 1:
#     ttk.Label(mainframe2, text='Shots Fired', width=25).grid(column=1, columnspan=5, row=6)

# def test(*args):
#     print("sucessfull test")
# ttk.Button(mainframe, text='test', command=test).grid(column=6, row=1)

root.mainloop()
rootthomas.mainloop()

