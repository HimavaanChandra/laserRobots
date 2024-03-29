#!/usr/bin/env python3
#!/usr/bin/env python2

import numpy as np
import random
import rospkg
import rospy
from tactics_ros.msg import tactics_comms_l
from map_ros.msg import map_comms

heading = 0
choice = 0
left_dis = 0 
front_left_dis = 0
front_dis = 0
front_right_dis = 0
right_dis = 0
back_dis = 0
my_x = 0
my_y = 0
enemy_x = 0
enemy_y = 0

pub = rospy.Publisher('robot_choice_l', tactics_comms_l, queue_size=10)
rospy.init_node('robot_choice_nodel', anonymous=True)
rate = rospy.Rate(10)  #10hz



def reader(data):
	global left_dis 
	global front_left_dis
	global front_dis
	global front_right_dis 
	global right_dis 
	global back_dis 
	global my_x
	global my_y 
	global enemy_x 
	global enemy_y 

	rospy.loginfo(data)
	left_dis = data.distances[0]
	front_left_dis = data.distances[1]
	front_dis = data.distances[2]
	front_right_dis = data.distances[3]
	right_dis = data.distances[4]
	back_dis = data.distances[5]
	my_x = data.xLightning
	my_y = data.yLightning
	enemy_x = data.xThomas
	enemy_y = data.yThomas
	

def get_inputs():

	global final_choice 
	global left_dis 
	global front_left_dis
	global front_dis
	global front_right_dis 
	global right_dis 
	global back_dis 
	global my_x
	global my_y 
	global enemy_x 
	global enemy_y 

	x_dif = my_x - enemy_x
	y_dif = my_y - enemy_y
	

	return[x_dif, y_dif, left_dis,front_left_dis, front_dis, front_right_dis, right_dis, back_dis]
	
def make_choice():
	inputs = get_inputs()

	x_dif_input = inputs[0]
	y_dif_input = inputs[1]
	left_dis = inputs[2]
	front_left_dis = inputs[3]
	front_dis = inputs[4]
	front_right_dis = inputs[5]
	right_dis = inputs[6]
	back_dis = inputs[7]

	if x_dif_input>-100 or x_dif_input<100:
		if y_dif_input>0:
			if (front_dis > 200 or front_right_dis>200 or front_left_dis>200) and (heading == 0 or heading == 45 or heading == -45):
				return 9
		elif y_dif_input<0:
			if (back_dis > 200) and (heading == 135 or heading == 180 or heading == -135):
				return 9

	if y_dif_input>-100 or y_dif_input<100:
		if x_dif_input>0:
			if (front_dis > 200 or front_right_dis>200 or front_left_dis>200) and (heading == 0 or heading == 45 or heading == -45):
				return 9
		elif x_dif_input<0:
			if (back_dis > 200) and (heading == 135 or heading == 180 or heading == -135):
				return 9

	# #what to do if enemy is at the same x-level
	# if x_dif_input==0:
	# 	random_factor = random.randint(0,1000) #chooses a number between 0-1000 to add randomness into the equation
	# 	if random_factor>970:
	# 		if (heading == 0 and y_dif_input>0):
	# 			if front_dis>200:
	# 				return 9
	# 			else:
	# 				choice = random.randint(1,8)
	# 				return choice
	# 		elif (heading == 180 or heading == -180 and y_dif_input<0):
	# 			if back_dis>200:
	# 				return 9
	# 			else:
	# 				choice = random.randint(1,8)
	# 				return choice
	# 		elif heading != 0 and y_dif_input>0:
	# 			return 1
	# 		elif heading != 0 and y_dif_input<0:
	# 			return 5
	# 	else:
	# 		choice = random.randint(1,8)
	# 		return choice

	#what to do if the enemy is to the right
	if x_dif_input>0:
		random_factor = random.randint(0,1000) #chooses a number between 0-1000 to add randomness into the equation
		if random_factor>970:
			if y_dif_input==0:
				if heading == 90 and right_dis > 100:
					return 9
				elif heading != 90 and right_dis >100:
					return 3
				elif heading != 90 and right_dis<100:
					if front_dis>back_dis:
						return 1
					else:
						return 5
				else:
					choice = random.randint(1,8)
					return choice
			else:
				if (heading>0 and heading<=180):
					if right_dis>200:
						choice = random.randint(2,4)
						return choice
				elif (heading<=0 and heading>180):
					if right_dis>=100:
						return 3
					elif right_dis<100:
						if front_dis>back_dis:
							return 1
						else:
							return 5
		else:
			choice = random.randint(1,8)
			return choice

	#what to do if the enemy is to the left
	if x_dif_input<0:
		random_factor = random.randint(0,1000) #chooses a number between 0-1000 to add randomness into the equation
		if random_factor>970:
			if y_dif_input==0:
				if heading == 90 and right_dis > 100:
					return 9
				elif heading != 90 and right_dis >100:
					return 3
				elif heading != 90 and right_dis<100:
					if front_dis>back_dis:
						return 1
					else:
						return 5
				else:
					choice = random.randint(1,8)
					return choice
			else:
				if (heading<0 and heading>=180):
					if left_dis>200:
						choice = random.randint(6,8)
						return choice
				elif (heading>=0 and heading<180):
					if left_dis>=100:
						return 3
					elif left_dis<100:
						if front_dis>back_dis:
							return 1
						else:
							return 2
		else:
			choice = random.randint(1,8)
			return choice
	return 0

def send_choice():
	global heading
	final_choice=None
	decision = make_choice()
	pre_heading = heading

	if decision == 0:
		final_choice="A"
		heading = pre_heading
	elif decision == 1:
		if front_dis < 50:
			if right_dis>left_dis:
				final_choice = "E"
				heading = 90
			else:
				final_choice = "W"
				heading = -90
		else:
			final_choice = "N"
			heading = 0
	elif decision == 2:
		if front_right_dis < 50:
			if right_dis>front_dis:
				final_choice = "E"
				heading = 90
			else:
				if front_dis>back_dis:
					final_choice = "N"
					heading = 0
				else:
					final_choice="SE"
					heading = 135
		else:
			final_choice = "NE"
			heading = 45
	elif decision == 3:
		if right_dis < 50:
			if back_dis>front_dis:
				final_choice = "S"
				heading = 180
			else:
				if front_dis>front_right_dis:
					final_choice = "N"
					heading = 0
				else:
					final_choice="NE"
					heading = 45
		else:
			final_choice = "E"
			heading = 90
	elif decision == 4:
		if back_dis < 50 or right_dis<50:
			if right_dis>front_right_dis:
				final_choice = "E"
				heading = 90
			else:
				final_choice="NE"
				heading = 45
		else:
			final_choice = "SE"
			heading = 135
	elif decision == 5:
		if back_dis < 50:
			if right_dis>left_dis:
				final_choice = "E"
				heading = 90
			else:
				final_choice="W"
				heading = -90
		else:
			final_choice = "S"
			heading = 180
	elif decision == 6:
		if back_dis < 50 or left_dis < 50:
			if left_dis>front_left_dis:
				final_choice = "W"
				heading = -90
			else:
				final_choice="NW"
				heading = -45
		else:
			final_choice = "SW"
			heading = -135
	elif decision == 7:
		if left_dis < 50:
			if back_dis>front_dis:
				final_choice = "S"
				heading = 180
			else:
				if front_dis>front_left_dis:
					final_choice = "N"
					heading = 0
				else:
					final_choice="NW"
					heading = -45
		else:
			final_choice = "W"
			heading = -90
	elif decision == 8:
		if front_left_dis < 50:
			if left_dis>front_dis:
				final_choice = "W"
				heading = -90
			else:
				if front_dis>back_dis:
					final_choice = "N"
					heading = 0
				else:
					final_choice="SW"
					heading = -135
		else:
			final_choice = "SW"
			heading = -45
	elif decision == 9:
		final_choice = "F"
		heading=pre_heading
	return final_choice



def main():

	final_choice = send_choice()
	print(final_choice)

	if not rospy.is_shutdown():
		msg = tactics_comms_l()
		msg.final_choice = final_choice
		rospy.loginfo(msg)
		pub.publish(msg)
		rate.sleep()  

rospy.Subscriber("map_chatter", map_comms, reader)

while(1):
	if __name__ =='__main__':
		main()