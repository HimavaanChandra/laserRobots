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

robot_position = None
respawn_point = None
scaling_factor = 200  # Scales down the grid to match Excel map size

cell_array = None

check = None


def callback(data):  # Updates robot position data when called
    global robot_position
    global respawn_point

    # rospy.loginfo(data)
    my_x = int(data.xThomas / scaling_factor)
    my_y = int(data.yThomas / scaling_factor)

    # my_x = int(data.xLightning / scaling_factor)
    # my_y = int(data.yLightning / scaling_factor)

    robot_position = (my_x, my_y)
    respawn_point = (0, 0)


def Print_Path(robot_position, respawn_point):
    # print("robot Pos" + str(robot_position))
    # maze, start, end - Object "aStar" sets start and coordinates for robot
    aStar = AStar(cell_array, robot_position, respawn_point)
    path = aStar.calculatePath()
    return path


class Node():  # Setting up "class" "Node"

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


class AStar():  # Setting up "class" "AStar"
    size = 1  # Sets the size of the buffer around the robot. MAKE SURE THAT ROBOT BUFFER IS NOT TOUCHING ANY WALLS IN THE STARTING POSITION
    # Initialisation function that is called when the class is called

    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end

    def setStart(self, start):  # Can be called using "aStar.setStart((#,#))" to set start positon
        self.start = start

    def setEnd(self, end):  # Can be called using "aStar.setEnd((#,#))" to set end positon
        self.end = end

    def calculatePath(self):  # Can be called using "path=aStar.calculatePath()" to run the "astar" function based on the predecided "maze, start and end" conditions
        return astar(self.maze, self.size, self.start, self.end)


def astar(maze, size, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    # Object sets starting position coordinates for robot
    start_node = Node(None, start)
    # Intialises "start_node" object values for g,h and f
    start_node.g = start_node.h = start_node.f = 0
    # Object sets ending position coordinates for robot
    end_node = Node(None, end)
    # Intialises "end_node" object values for g,h and f
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node to the open list (Acts as the initial parent node ---> moved to the parent loop later in code)
    open_list.append(start_node)

    # Loop while the open list still has nodes present
    while len(open_list) > 0:

        # print(len(open_list)) # Added for a testing readout of the current "open_list" value

        # Get the current node
        # Adds current node to index position 0, shifting other open list nodes to the "right"
        current_node = open_list[0]
        current_index = 0
        # cycles through each index value in the "open_list"
        for index, item in enumerate(open_list):
            # Linking F Value of each 'OpenList" node to the "start_node" object. If F value of any node in the open list is less than the current node. Set it to be the PARENT NODE (move previous parent node to the closed list)
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        # Remove lowest F Value node from the open list (When start_mode removed from open_list move it to the closed_list)
        open_list.pop(current_index)
        # Add lowest F Value node to the end of the closed list as a PARENT NODE
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []  # Creating a list for creating the final path
            # linking "current" to "current_node = open_list[0]"
            current = current_node
            while current is not None:  # "None" is similar to "NULL" in C coding maybe???
                # Note to self ---> modifier = path[]
                # "current.position" links to the object "new_node = Node(current_node, node_position)" further down in code - # Add the "current.position" to the end of the "path"
                path.append(current.position)
                # Note to self ---> (path = path - modifier) ---> (SHOULD GIVE THE CHANGE IN COORDINATE VALUE?? E.G. (3,1)-(2,1) ---> (1,0) = 1 GRID UPWARDS)
                # "current.parent" links to the object "new_node = Node(current_node, node_position)" further down in code
                current = current.parent

            directions = []
            # Converts each co-ordinate in the path into a direction/bearing
            for i in range(0, len(path)):
                if i == 0:
                    continue
                # path[i][0] == x, path[i][1] == y - Minuses the previous coordinate from each coordinate to get a unit vector
                unit_vector = (path[i-1][0] - path[i][0],
                               path[i-1][1] - path[i][1])

                # Bearing(0)

                if unit_vector == (0, -1):
                    unit_vector = "N"
                elif unit_vector == (1, -1):
                    unit_vector = "NE"
                elif unit_vector == (1, 0):
                    unit_vector = "E"
                elif unit_vector == (1, 1):
                    unit_vector = "SE"
                elif unit_vector == (0, 1):
                    unit_vector = "S"
                elif unit_vector == (-1, 1):
                    unit_vector = "SW"
                elif unit_vector == (-1, 0):
                    unit_vector = "W"
                elif unit_vector == (-1, -1):
                    unit_vector = "NW"
                elif unit_vector == (0, 0):
                    unit_vector = "A"

                # Repeats each direction 5 times for each movement. This gives the required resolution to the stepper motor/movement code
                for x in range(5):
                    directions.append(unit_vector)

            # return path[::-1]  # Return reversed path
            return directions[::-1]  # Return reversed path

        # Generate children nodes from around the parent
        children = []
        # Adjacent squares
        # List (Position 0 = y, Positon 1 = x) creating 8 children for each grid space around a parent grid (In order: left, right, down, top, bottom left, top left, bottom right, top right)
        for new_position in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:

            # Get node position
            # "current_node.position" links to the object "new_node = Node(current_node, node_position)" further down in code
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # If the current node is already on the closed list. No need to add it to the open list to be checked again
            if Node(current_node, node_position) in closed_list:
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
            if new_position == (1, 1):  # SE bearing
                # Checking in the location of the hashes *# "*" = SE Movement
                if maze[node_position[1] - 1][node_position[0]]:
                    continue  # *
                if maze[node_position[1]][node_position[0] - 1]:
                    continue
            elif new_position == (1, -1):  # NE bearing
                if maze[node_position[1]][node_position[0] - 1]:
                    continue
                if maze[node_position[1] + 1][node_position[0]]:
                    continue
            elif new_position == (-1, -1):  # NW bearing
                if maze[node_position[1]][node_position[0] + 1]:
                    continue
                if maze[node_position[1] + 1][node_position[0]]:
                    continue
            elif new_position == (-1, 1):  # SW bearing
                if maze[node_position[1]][node_position[0] + 1]:
                    continue
                if maze[node_position[1] - 1][node_position[0]]:
                    continue

            # Create new node
            # Creating object for new child node that allows "current.parent" property to be called when the goal is found
            new_node = Node(current_node, node_position)

            # Append
            # Adding each of the 8 new children nodes to the end of the "children" list
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is already in the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    break
            else:
                # Create the f, g, and h values
                # "child.position" = new postion, "current_node.position" = current positon
                distance = abs(child.position[1] - current_node.position[1]) + abs(
                    child.position[0] - current_node.position[0])
                if (distance > 1):
                    # child.g = current_node.g + 3 # G Value cost of 3 (approx = hypotenuse = sqrt(8) = 2.828) diagonal positon moved
                    child.g = current_node.g + 3
                else:
                    # child.g = current_node.g + 2 # G Value cost of 2 per horizontal or vertical positon moved
                    child.g = current_node.g + 2

                # child.position uses the "new_node" object that has been appended into the children list
                # Child positon 0 = y Child positon 1 = x - GIVES X + Y DISTANCE FROM END GOAL
                child.h = abs(child.position[1] - end_node.position[1]) + \
                    abs(child.position[0] - end_node.position[0])
                child.f = child.g + child.h  # F=G+H = MOVEMENT COST

                # Child is already in the open list
                for open_node in open_list:
                    # check if the new path to children is worse or equal
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break  # If the new node is slower then break?
                else:
                    # Add the child to the open list
                    # This also link "current_node" to the "new_node" object as "current_node = open_list[0]"??
                    open_list.append(child)


def main():

    global check

    path = Print_Path(robot_position, respawn_point)

    if check == path: # When robot position is   constant
        return

    else: # When robot position changes

        for path_item in path:  # Set path_item to each iterative index in path
            if not rospy.is_shutdown():
                msg = astar_comms()
                msg.path = path_item  # message being published
                rospy.loginfo(msg)
                pub.publish(msg)
                rate.sleep()
            check = path
        # # spin() simply keeps python from exiting until this node is stopped
        # rospy.spin() # Acts like a while loop to continually check for chatter

        print("Path" + str(path))  # Prints coordinates of path to terminal

if __name__ == '__main__':  # So that when/if this file is created as a header file. Only the main loop of the overall file

    # Publisher (outputs compass bearing directions)
    pub = rospy.Publisher('astar_path', astar_comms,
                          queue_size=10)  # Topic Name
    rospy.init_node('astar_node', anonymous=True)  # Node Name
    rate = rospy.Rate(10)  # 10hz

    # Subscriber (subscribed to map_comms robot coordiante output)
    rospy.Subscriber("map_chatter", map_comms, callback)

    # Create map from .csv (Excel)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cell_map = np.loadtxt(dir_path + "/" + "filename.csv", delimiter=",")
    cell_array = np.array(cell_map).tolist()

    while True:
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
