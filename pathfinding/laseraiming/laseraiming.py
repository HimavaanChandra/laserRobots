'''
Laser Aiming Code

Code Author: Thomas Harrison
Date: ##/##/2019

# Update every time a robot moves or rotates
# Aiming_Angles are with respect to the postive x axis (East - with North being the front of the robot)

'''

import math

def Laser_Aiming_Angle (My_Position, Enemy_Position):

    if My_Position[0] > Enemy_Position[0] and My_Position[1] > Enemy_Position[1]: # [0] = x [1] = y
        
        x = My_Position[0] - Enemy_Position[0]
        y = My_Position[1] - Enemy_Position[1]
        
        Aiming_Angle = int(180-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    elif My_Position[0] < Enemy_Position[0] and My_Position[1] > Enemy_Position[1]:
        
        x = My_Position[0] - Enemy_Position[0]
        y = My_Position[1] - Enemy_Position[1]
        
        Aiming_Angle = int(-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    elif My_Position[0] < Enemy_Position[0] and My_Position[1] < Enemy_Position[1]:
        
        x = My_Position[0] - Enemy_Position[0]
        y = My_Position[1] - Enemy_Position[1]
        
        Aiming_Angle = int(360-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down

    else: # My_Position[0] > Enemy_Position[0] and My_Position[1] < Enemy_Position[1]

        x = My_Position[0] - Enemy_Position[0]
        y = My_Position[1] - Enemy_Position[1]
        
        Aiming_Angle = int(180-math.degrees(math.atan(y/x))) # Slight inncauracy due to int always rounding down
    
    Distance = (-x, -y) # Red robot with respect to the blue robot

    print('Distance (My Position WRT Enemy Position):', Distance)
    print('Aiming_Angle:', Aiming_Angle)
    
    return Aiming_Angle
    
# # Robot Rotation Compensation

# Blue_Robot_Rotation_Aiming_Angle = +0 # Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?
# Red_Robot_Rotation_Aiming_Angle = +0 # Positive = clockwise, Negative = counter clockwise, North facing robot = 0 degrees?

# Aiming_Angle = Aiming_Angle + Blue_Robot_Rotation_Aiming_Angle
# Red_Aiming_Angle = Red_Aiming_Angle + Red_Robot_Rotation_Aiming_Angle

# if Aiming_Angle > 360:
#     Aiming_Angle = Aiming_Angle % 360

# elif Aiming_Angle < 0:
#     Aiming_Angle = Aiming_Angle % 360

# if Red_Aiming_Angle > 360:
#     Red_Aiming_Angle = Red_Aiming_Angle % 360

# elif Red_Aiming_Angle < 0:
#     Red_Aiming_Angle = Red_Aiming_Angle % 360

Laser_Aiming_Angle((0, 0),(12, 8)) # My Position, Enemy Position


