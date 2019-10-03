import threading
# import json

from entity import Line, Point
from collision import Collision
from game import Wall, WallContainer, Robot
from config import SCALE, DEBUG


class SimLayer():
    def __init__(self, grid):
        self.wall_container = None
        self.instances = []
        self.scale = SCALE
        self.size = 90
        self.spawn_wall_container(grid)

    def spawn_wall_container(self, grid):
        self.wall_container = WallContainer(
            len(grid[0])*self.scale,
            len(grid)*self.scale
        )

        for row_i in range(0, len(grid)):
            for cell_i in range(0, len(grid[row_i])):
                cell = grid[row_i][cell_i]
                if cell == 1:
                    y_1 = row_i * self.scale
                    y_2 = y_1 + self.scale
                    x_1 = cell_i * self.scale
                    x_2 = x_1 + self.scale

                    self.wall_container.add(Wall(x_1, y_1, x_2, y_2))

    def spawn_instance(self, name):
        new_instance = SimThread(self.wall_container, self.size)
        new_instance.start()
        new_instance.setName(name)

        self.instances.append(new_instance)
        return new_instance


class SimThread(threading.Thread):
    def __init__(self, wall_container, size):
        super().__init__()
        self.robots = []
        self.size = size
        self.wall_container = wall_container
        self.line_of_sight = None

    def spawn_robots(self, x1, y1, x2, y2):
        robot1 = Robot(x1, y1, x1 + self.size, y1 + self.size)
        robot2 = Robot(x2, y2, x2 + self.size, y2 + self.size)

        self.robots.clear()
        self.robots.append(robot1)
        self.robots.append(robot2)
        self.update()

    def move(self, index, m_vector):
        if len(self.robots) > index:
            if not (m_vector[0] == 0 and m_vector[1] == 0):
                self.robots[index].move(m_vector, self.wall_container)
                self.update()
        # if len(self.robots) > index:
        #     if m_vector[0] != 0 and m_vector[1] != 0:
        #         self.robots[index].move(m_vector, self.wall_container)
        #         self.update()

    def set(self, index, s_vector):
        if len(self.robots) > index:
            self.robots[index].set(s_vector)
            self.update()

    def update(self):
        self.line_of_sight = Line(
            Point(vector=self.robots[0].center),
            Point(vector=self.robots[1].center)
        )
        self.line_of_sight.update()

    def data(self, index):
        robot = self.robots[index]
        distance = robot.distance(self.wall_container)
        enemy = self.robots[len(self.robots) - index - 1]
        can_shoot = not self.wall_container.check_line_collision(
            self.line_of_sight
        )

        data = (
            '{'
            '"can_shoot":' + str(can_shoot).lower() + ','
            '"line_of_sight": [' + str(self.line_of_sight) + '],'
            '"distances":' + str(distance) + ','
            '"player_x":' + str(robot.center[0]) + ','
            '"player_y":' + str(robot.center[1]) + ','
            '"enemy_x":' + str(enemy.center[0]) + ','
            '"enemy_y":' + str(enemy.center[1]) +
            '}'
        )
        return data

    def debug_draw(self, screen):
        if DEBUG:
            self.wall_container.debug_draw(screen)
            for robot in self.robots:
                robot.debug_draw(screen)
            Collision.debug_draw(screen)

            self.line_of_sight.debug_draw(screen, (255, 255, 255))
