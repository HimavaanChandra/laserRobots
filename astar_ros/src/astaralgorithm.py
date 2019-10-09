#!/usr/bin/env python2
#!/usr/bin/env python3

import os
import rospkg
import rospy
from map_ros.msg import map_comms
from astar_ros.msg import astar_comms

import numpy as np
from numpy import genfromtxt
import operator

cell_array = None

# Publisher
pub = rospy.Publisher('astar_path', astar_comms, queue_size=10) # Topic Name
rospy.init_node('astar_path', anonymous=True) # Node Name
rate = rospy.Rate(10) # 10hz

def callback(data):

    global my_x
    global my_y
    global enemy_x
    global enemy_y
    global robot_position
    global respawn_point

    rospy.loginfo(data)
    my_x = data.xThomas
    my_y = data.yThomas
    
    # my_x = data.xLightning
    # my_y = data.yLightning

    robot_position = (my_x, my_y)
    respawn_point = (0,0)

def Print_Path(robot_position, respawn_point):
   
    global path

    global cell_array
    aStar = AStar(cell_array, robot_position, respawn_point) # maze, start, end - Object "aStar" sets start and coordinates for robot
    path=aStar.calculatePath() 
    print(path) # Prints coordinates of path to terminal

# def callback(data): # Runs when what I am subscribed to publishes something
#     rospy.loginfo("xThomas %d : yThomas %d" % (data.xThomas, data.yThomas))
#     rospy.loginfo("xLightning %d : yLightning %d" % (data.xLightning, data.yLightning))
    
#     Print_Path((data.xThomas, data.yThomas ), (0,0)) # robot_position, respawn_point

class Node(): # Setting up "class" "Node"

    """A node class for A* Pathfinding"""

    # Initialisation function that is called when the class is called
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0  # G Value
        self.h = 0  # Heuristic Value
        self.f = 0  # F Value = G Value + Heuristic Value

    def __eq__(self, other):
        return self.position == other.position

class AStar(): #Setting up "class" "AStar"
    size = 1 #Sets the size of the buffer around the robot. MAKE SURE THAT ROBOT BUFFER IS NOT TOUCHING ANY WALLS IN THE STARTING POSITION
    # Initialisation function that is called when the class is called
    def __init__(self, maze, start, end): 
        self.maze = maze
        self.start = start
        self.end=end

    def setStart(self, start): # Can be called using "aStar.setStart((#,#))" to set start positon
        self.start=start
        
    def setEnd(self, end): # Can be called using "aStar.setEnd((#,#))" to set end positon
        self.end=end
        
    def calculatePath(self): # Can be called using "path=aStar.calculatePath()" to run the "astar" function based on the predecided "maze, start and end" conditions
        return astar(self.maze, self.size, self.start, self.end)

# unit_vector = None # Variable must exist in global namespace first

# def Bearing(bearing_mode): #COMPASS MODE = 0, DEGREES MODE = 1

#     global unit_vector #this creates a local variable that is linked to the global variable
    
#     if bearing_mode == 0:
#         if  unit_vector == (0,-1): 
#             unit_vector='N'
#         elif unit_vector == (1,-1): 
#             unit_vector='NE'
#         elif unit_vector == (1,0): 
#             unit_vector='E'
#         elif unit_vector == (1,1): 
#             unit_vector='SE'    
#         elif unit_vector == (0,1):
#             unit_vector='S'
#         elif unit_vector == (-1,1):
#             unit_vector='SW'
#         elif unit_vector == (-1,0):
#             unit_vector='W'
#         elif unit_vector == (-1,-1): 
#             unit_vector='NW'
#         elif unit_vector == (0,0): 
#             unit_vector='NONE'

#     elif bearing_mode == 1:
#         if unit_vector == (0,-1): 
#             unit_vector='0'
#         elif unit_vector == (1,-1): 
#             unit_vector='45'
#         elif unit_vector == (1,0): 
#             unit_vector='90'
#         elif unit_vector == (1,1): 
#             unit_vector='135'    
#         elif unit_vector == (0,1):
#             unit_vector='180'
#         elif unit_vector == (-1,1):
#             unit_vector='225'
#         elif unit_vector == (-1,0):
#             unit_vector='270'
#         elif unit_vector == (-1,-1): 
#             unit_vector='315'
#         elif unit_vector == (0,0): 
#             unit_vector='NONE'

    

def astar(maze, size, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start) # Object sets starting position coordinates for robot
    start_node.g = start_node.h = start_node.f = 0 # Intialises "start_node" object values for g,h and f
    end_node = Node(None, end)  # Object sets ending position coordinates for robot
    end_node.g = end_node.h = end_node.f = 0 # Intialises "end_node" object values for g,h and f

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node to the open list (Acts as the initial parent node ---> moved to the parent loop later in code)
    open_list.append(start_node) 

    # Loop while the open list still has nodes present
    while len(open_list) > 0:
        
        print(len(open_list)) # Added for a testing readout of the current "open_list" value
       
        # Get the current node
        current_node = open_list[0] # Adds current node to index position 0, shifting other open list nodes to the "right"
        current_index = 0 
        for index, item in enumerate(open_list): # cycles through each index value in the "open_list"
            if item.f < current_node.f: #Linking F Value of each 'OpenList" node to the "start_node" object. If F value of any node in the open list is less than the current node. Set it to be the PARENT NODE (move previous parent node to the closed list)
                current_node = item 
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index) # Remove lowest F Value node from the open list (When start_mode removed from open_list move it to the closed_list)
        closed_list.append(current_node) # Add lowest F Value node to the end of the closed list as a PARENT NODE

        # Found the goal
        if current_node == end_node:
            path = [] #Creating a list for creating the final path
            current = current_node #linking "current" to "current_node = open_list[0]"
            while current is not None: # "None" is similar to "NULL" in C coding maybe???
                #Note to self ---> modifier = path[] 
                path.append(current.position) # "current.position" links to the object "new_node = Node(current_node, node_position)" further down in code - # Add the "current.position" to the end of the "path"
                #Note to self ---> (path = path - modifier) ---> (SHOULD GIVE THE CHANGE IN COORDINATE VALUE?? E.G. (3,1)-(2,1) ---> (1,0) = 1 GRID UPWARDS)
                current = current.parent #"current.parent" links to the object "new_node = Node(current_node, node_position)" further down in code
            
            directions = []
            for i in range(0, len(path)): # Converts each co-ordinate in the path into a direction/bearing
                if i == 0:
                    continue
                unit_vector = (path[i-1][0] - path[i][0], path[i-1][1] - path[i][1]) #path[i][0] == x, path[i][1] == y - Minuses the previous coordinate from each coordinate to get a unit vector
                
                # Bearing(0)
                
                if  unit_vector == (0,-1): 
                    unit_vector='N'
                elif unit_vector == (1,-1): 
                    unit_vector='NE'
                elif unit_vector == (1,0): 
                    unit_vector='E'
                elif unit_vector == (1,1): 
                    unit_vector='SE'    
                elif unit_vector == (0,1):
                    unit_vector='S'
                elif unit_vector == (-1,1):
                    unit_vector='SW'
                elif unit_vector == (-1,0):
                    unit_vector='W'
                elif unit_vector == (-1,-1): 
                    unit_vector='NW'
                elif unit_vector == (0,0): 
                    unit_vector='NONE'
                
                for x in range(5): # Repeats each direction 5 times for each movement. This gives the required resolution to the stepper motor/movement code
                    directions.append(unit_vector)

            # return path[::-1]  # Return reversed path
            return directions[::-1]  # Return reversed path

        # Generate children nodes from around the parent
        children = []
        # Adjacent squares
        for new_position in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]: # List (Position 0 = y, Positon 1 = x) creating 8 children for each grid space around a parent grid (In order: left, right, down, top, bottom left, top left, bottom right, top right) 
            
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]) #"current_node.position" links to the object "new_node = Node(current_node, node_position)" further down in code

            #If the current node is already on the closed list. No need to add it to the open list to be checked again
            if Node(current_node,node_position) in closed_list: 
                continue 

            # Make sure within range of maze 
            if node_position[1] > (len(maze) - 1) or node_position[1] < 0 or node_position[0] > (len(maze[len(maze)-1]) - 1) or node_position[0] < 0:
                continue

            # Make sure new postion is walkable terrain (Not in a wall)
            if maze[node_position[1]][node_position[0]] != 0:
                continue

            # 0 = x and 1 = y
            # Below is a corner crossing wall check
            # If the new position is on a diagnoal, only consider it if there are no walls on either side of the node positon after the movement
            if new_position == (1, 1): # SE bearing 
                if maze[node_position[1] - 1][node_position[0]]: # Checking in the location of the hashes *# "*" = SE Movement
                    continue                                                                              #*
                if maze[node_position[1]][node_position[0] - 1]: # 
                    continue        
            elif new_position == (1, -1): # NE bearing
                if maze[node_position[1]][node_position[0] - 1]:
                    continue
                if maze[node_position[1] + 1][node_position[0]]:
                    continue
            elif new_position == (-1, -1): # NW bearing 
                if maze[node_position[1]][node_position[0] + 1]:
                    continue
                if maze[node_position[1] + 1][node_position[0]]:
                    continue
            elif new_position == (-1, 1): # SW bearing
                if maze[node_position[1]][node_position[0] + 1]:
                    continue
                if maze[node_position[1] - 1][node_position[0]]:
                    continue

            # # Map range check
            # out_range = False     
            # if node_position[1]+size > (len(maze) - 1) or node_position[1]+size < 0 or node_position[0]+size > (len(maze[len(maze)-1]) - 1) or node_position[0]+size < 0: # Diagonal from bottom left to top right
            #     out_range = True

            # # If not in map
            # if out_range == True:
            #     continue
            
            # # Below is a wall check
            # collision = False
            # for x in range(-size, size):
            #     # Ignore zero since it is already checked
            #     if x == 0:
            #         continue

            #     # Diagonal from bottom left to top right
            #     if maze[node_position[1]+x][node_position[0]+x] != 0: # != 0 = 1 = if wall present
            #         collision = True  
            #     # Diagonal from top left to bottom right
            #     elif maze[node_position[1]+x][node_position[0]-x] != 0:
            #         collision = True
            #     # Horizontal
            #     elif maze[node_position[1]+x][node_position[0]] != 0:
            #         collision = True 
            #     # Vertical
            #     elif maze[node_position[1]][node_position[0]+x] != 0:
            #         collision = True
            
            # # If wall present
            # if collision == True:
            #     continue

            # Create new node
            new_node = Node(current_node, node_position) # Creating object for new child node that allows "current.parent" property to be called when the goal is found 

            # Append
            children.append(new_node) # Adding each of the 8 new children nodes to the end of the "children" list

        # Loop through children
        for child in children:
            # Child is already in the closed list
            for closed_child in closed_list:
                if child == closed_child: 
                    break
            else:
                # Create the f, g, and h values
                distance = abs(child.position[1] - current_node.position[1]) + abs(child.position[0] - current_node.position[0]) # "child.position" = new postion, "current_node.position" = current positon
                if (distance > 1):
                    child.g = current_node.g + 3 # child.g = current_node.g + 3 # G Value cost of 3 (approx = hypotenuse = sqrt(8) = 2.828) diagonal positon moved 
                else:
                    child.g = current_node.g + 2 # child.g = current_node.g + 2 # G Value cost of 2 per horizontal or vertical positon moved
                
                # child.position uses the "new_node" object that has been appended into the children list
                child.h = abs(child.position[1] - end_node.position[1]) + abs(child.position[0] - end_node.position[0])  #Child positon 0 = y Child positon 1 = x - GIVES X + Y DISTANCE FROM END GOAL
                child.f = child.g + child.h #F=G+H = MOVEMENT COST

                # Child is already in the open list
                for open_node in open_list:
                    # check if the new path to children is worse or equal 
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g: 
                        break #If the new node is slower then break?
                else:
                    # Add the child to the open list
                    open_list.append(child) #This also link "current_node" to the "new_node" object as "current_node = open_list[0]"??

def main():

    # rospy.init_node('astar_listener', anonymous=True) 
    # rospy.Subscriber("map_chatter", map_comms, callback) # Listening to subscriber information

    if not rospy.is_shutdown():
            msg = astar_comms()
            msg.path = path # message being published
            rospy.loginfo(msg)
            pub.publish(msg)
            rate.sleep()  

    rospy.Subscriber("map_chatter", map_comms, callback)

    # # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin() # Acts like a while loop to continually check for chatter

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cell_map = np.loadtxt(dir_path + "/" + "filename.csv", delimiter=",")
    cell_array = np.array(cell_map).tolist()

    Print_Path(robot_position, respawn_point)


while(1):   
    if __name__ == '__main__': #So that when/if this file is created as a header file. Only the main loop of the overall file will be executed
        main()







    # maze = np.genfromtxt('filename.csv', delimiter=',')
    
    # MULTI DIMENSIONAL (2D) 41x41 ARRAY (INCLUDING 0) (ARRAYS WITHIN AN ARRAY)
    # x-axis 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
    # maze = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0 y-axis
    #         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #1
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #2
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #3
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #4
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #5
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #6
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7
    #         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #8
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #10
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #11
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], #12
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], #13
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #14
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #15
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #16
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #17
    #         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0], #18
    #         [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #19
    #         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #20
    #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #21
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #22
    #         [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #23
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #24
    #         [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #25
    #         [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #26
    #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #27
    #         [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #28
    #         [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #29
    #         [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #30
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], #31
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], #32
    #         [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], #33
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], #34
    #         [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #35
    #         [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], #36
    #         [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #37
    #         [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #38
    #         [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], #39 
    #         [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #40
