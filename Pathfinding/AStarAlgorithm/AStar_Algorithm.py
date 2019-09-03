'''
A* Algorithm Code

Original code Author: Nicholas Swift
Date: 28/02/2017 
Nicholas Swift "Easy A* (star) Pathfinding" webpage: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Nicholas Swift Github: https://github.com/Nicholas-Swift

Modifications: Thomas Harrison
Date: ##/##/2019

'''

class Node(): #Setting up "class" "Node"

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

    # Initialisation function that is called when the class is called
    def __init__(self, maze, start, end): 
        self.maze = maze
        self.start = start
        self.end=end

    def setStart(self, start): #Can be called using "aStar.setStart((#,#))" to set start positon
        self.start=start
        
    def setEnd(self, end): #Can be called using "aStar.setEnd((#,#))" to set end positon
        self.end=end
        
    def calculatePath(self): #Can be called using "path=aStar.calculatePath()" to run the "astar" function based on the predecided "maze, start and end" conditions
        return astar(self.maze, self.start, self.end)

def astar(maze, start, end):
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
                path.append(current.position) #"current.position" links to the object "new_node = Node(current_node, node_position)" further down in code - # Add the "current.position" to the end of the "path"
                #Note to self ---> (path = path - modifier) ---> (SHOULD GIVE THE CHANGE IN COORDINATE VALUE?? E.G. (3,1)-(2,1) ---> (1,0) = 1 GRID UPWARDS)
                current = current.parent #"current.parent" links to the object "new_node = Node(current_node, node_position)" further down in code
            return path[::-1]  # Return reversed path

        # Generate children nodes from around the parent
        children = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # List (Position 0 = x, Positon 1 = y) creating 8 children for each grid space around a parent grid (In order: left, right, down, top, bottom left, top left, bottom right, top right) 
            
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]) #"current_node.position" links to the object "new_node = Node(current_node, node_position)" further down in code

            #If the current node is already on the closed list. No need to add it to the open list to be checked again
            if Node(current_node,node_position) in closed_list: 
                continue 

            # Make sure within range of maze 
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain (Not in a wall)
            if maze[node_position[0]][node_position[1]] != 0:
                continue

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
                child.g = current_node.g + 1 #G Value cost of 1 per positon moved
                # child.position uses the "new_node" object that has been appended into the children list
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])  #Child positon 0 = x Child positon 1 = y - USING PYTHAGORS'S THEREOM (HYPOTENEUS)
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

    # MULTI DIMENSIONAL (2D) 41x41 ARRAY (INCLUDING 0) (ARRAYS WITHIN AN ARRAY)
    #        0  1  2  3  4  5  6  7  8  9 .......... 
    maze = [[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # x1=0
    # y1=0
    
    # x2=40
    # y2=45

    # max = 40

    # while maze == 1:
    #     if x1 or y1 < max:
    #         x1+=1
    #         y1+=1
    #     else:
    #         x1-=1
    #         y1-=1
        
    # while maze == 1:
    #     if x2 or y2 < max:
    #         x2+=1
    #         y2+=1
    #     else:
    #         x2-=1
    #         y2-=1
   
    aStar = AStar(maze, (0, 0), (40, 40)) # maze, start, end - Object "aStar" sets start and coordinates for robot
    path=aStar.calculatePath() 
    print(path) #Prints coordinates of path to terminal
    aStar.setStart((40, 40)) #Sets start positon (Should be set to equal previous path end position)
    aStar.setEnd((7,7)) #Sets end positon
    path=aStar.calculatePath() #Run the "astar" function based on the predecided "maze, start and end" conditions
    print(path) #Prints coordinates of path to terminal
        
if __name__ == '__main__': #So that when/if this file is created as a header file. Only the main loop of the overall file will be executed
    main()
