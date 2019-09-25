'''
Laser Aiming Code

Code Author: Thomas Harrison
Date: ##/##/2019

# Update every time a robot moves or rotates
# Angles are with respect to the postive x axis (East - with North being the front of the robot)

'''

import math

def Blue_Laser_Aiming_Angles (Blue_Position, Red_Position):

    if Blue_Position[0] > Red_Position[0] and Blue_Position[1] > Red_Position[1]: # [0] = x [1] = y
        
        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Blue_Angle = int(180-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    elif Blue_Position[0] < Red_Position[0] and Blue_Position[1] > Red_Position[1]:
        
        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Blue_Angle = int(-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    elif Blue_Position[0] < Red_Position[0] and Blue_Position[1] < Red_Position[1]:
        
        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Blue_Angle = int(360-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    else: # Blue_Position[0] > Red_Position[0] and Blue_Position[1] < Red_Position[1]

        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Blue_Angle = int(180-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down
    
    Distance = (-x, -y) # Red robot with respect to the blue robot

    print('Distance (Red WRT Blue):', Distance)
    print('Blue Angle:', Blue_Angle)
    
    return Blue_Angle

def Red_Laser_Aiming_Angles (Blue_Position, Red_Position):

    if Blue_Position[0] > Red_Position[0] and Blue_Position[1] > Red_Position[1]: # [0] = x [1] = y
        
        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Red_Angle = int(360-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    elif Blue_Position[0] < Red_Position[0] and Blue_Position[1] > Red_Position[1]:
        
        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Red_Angle = int(180-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    elif Blue_Position[0] < Red_Position[0] and Blue_Position[1] < Red_Position[1]:
        
        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Red_Angle = int(180-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    else: # Blue_Position[0] > Red_Position[0] and Blue_Position[1] < Red_Position[1]

        x = Blue_Position[0] - Red_Position[0]
        y = Blue_Position[1] - Red_Position[1]
        
        Red_Angle = int(-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    Distance = (x, y) # Blue robot with respect to the red robot

    print('Distance (Blue WRT Red):', Distance)
    print('Red Angle:', Red_Angle)

    return Red_Angle
    
# # Robot Rotation Compensation

# Blue_Robot_Rotation_Angle = +0 # Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?
# Red_Robot_Rotation_Angle = +0 # Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?

# Blue_Angle = Blue_Angle + Blue_Robot_Rotation_Angle
# Red_Angle = Red_Angle + Red_Robot_Rotation_Angle

# if Blue_Angle > 360:
#     Blue_Angle = Blue_Angle % 360

# elif Blue_Angle < 0:
#     Blue_Angle = Blue_Angle % 360

# if Red_Angle > 360:
#     Red_Angle = Red_Angle % 360

# elif Red_Angle < 0:
#     Red_Angle = Red_Angle % 360

Blue_Laser_Aiming_Angles((0, 0),(12, 8)) # Blue_Postion, Red_Position

Red_Laser_Aiming_Angles((0, 0),(12, 8)) # Blue_Postion, Red_Position


