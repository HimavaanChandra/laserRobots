#!/usr/bin/env python3
import pygame as pygame
import math

from entity import Square, Line, Point
from collision import Collision
from config import DEBUG


class Wall(Square):
    """Wall, extends Square"""

    def __init__(self, x_1, y_1, x_2, y_2, point1=None, point2=None):
        if point1 is None and point2 is None:
            point1 = Point(x_1, y_1)
            point2 = Point(x_2, y_2)

        super().__init__(point1, point2)
        self.sprite = self.generate_sprite((125, 0, 125))


class WallContainer():
    """Container for the walls"""

    def __init__(self, size_x, size_y):
        self.walls = []
        # Create slightly oversized map container
        self.container = Square(Point(-1, -1), Point(size_x + 1, size_y + 1))
        self.wall_sprites = pygame.sprite.Group()

    def add(self, wall):
        self.walls.append(wall)
        self.wall_sprites.add(wall.sprite)

    def check_line_collision(self, test_line):
        collisions = []
        for wall in self.walls:
            result = wall.check_line_collision(test_line)
            if result is not False:
                collisions += result
        if not collisions:
            return False
        else:
            return collisions

    def check_square_collision(self, test_square):
        collisions = []
        for wall in self.walls:
            result = wall.check_square_collision(test_square)
            if result is not False:
                collisions += result
        if not collisions:
            return False
        else:
            return collisions

    def debug_draw(self, screen):
        if DEBUG is True:
            for wall in self.walls:
                wall.debug_draw(screen)
                # print("Wall: " + str(wall))


class Robot(Square):
    def __init__(self, x_1, y_1, x_2, y_2, point1=None, point2=None):
        if point1 is None and point2 is None:
            point1 = Point(x_1, y_1)
            point2 = Point(x_2, y_2)

        self.distance_lines = []
        super().__init__(point1, point2)
        self.sprite = self.generate_sprite((0, 125, 125))
        self._generate_distance_lines()

    def _generate_distance_line(self, origin, offset):
        start = origin
        end = [
            origin[0] + offset[0],
            origin[1] + offset[1]
        ]
        line = Line(Point(vector=start), Point(vector=end))
        return line

    def _generate_distance_lines(self):
        center = self.center
        length = 500

        left = self._generate_distance_line(center, [0, length])
        left_up = self._generate_distance_line(center, [length, length])
        right = self._generate_distance_line(center, [0, -length])
        right_up = self._generate_distance_line(center, [length, -length])
        up = self._generate_distance_line(center, [length, 0])
        left_down = self._generate_distance_line(center, [-length, length])
        down = self._generate_distance_line(center, [-length, 0])
        right_down = self._generate_distance_line(center, [-length, -length])

        self.distance_lines.clear()
        self.distance_lines.append(left)
        self.distance_lines.append(left_up)
        self.distance_lines.append(up)
        self.distance_lines.append(right_up)
        self.distance_lines.append(right)        
        self.distance_lines.append(right_down)
        self.distance_lines.append(down)
        self.distance_lines.append(left_down)

    def move(self, m_vector, wall_container):
        super().move(m_vector)

        if Collision.square_square(wall_container.container, self) is not False:
            super().move([
                - m_vector[0],
                - m_vector[1]
            ])
        elif wall_container.check_square_collision(self) is not False:
            super().move([
                - m_vector[0],
                - m_vector[1]
            ])
        else:
            # No Collisions
            self.update()
            # Move Distance Lines
            for line in self.distance_lines:
                line.move(m_vector)

    def set(self, s_vector):
        super().set(s_vector)
        for line in self.distance_lines:
            line.set(self.center)
            line.update()
        self.update()

    def update(self):
        super().update()
        if self.sprite is not None:
            # Move Sprite Rectangle
            self.sprite.rect.x = self.origin[0]
            self.sprite.rect.y = self.origin[1]

    def distance(self, wall_container):
        center = self.center
        distances = []

        for line in self.distance_lines:
            result = wall_container.check_line_collision(line)
            if result is not False:
                collision_distances = []
                for collision in result:
                    point1 = collision.start.vector
                    point2 = collision.end.vector

                    a = point1[1] - point2[1]
                    b = point2[0] - point1[0]
                    c = -b * point1[1] - a * point1[0]

                    numerator = a * center[0] + b * center[1] + c
                    denominator = math.sqrt((a)**2 + (b)**2)

                    collision_distance = abs(numerator / denominator)

                    # collision_distance = np.divide(
                    #     np.abs(np.cross(
                    #         point2 - point1,
                    #         point1 - origin
                    #     )),
                    #     np.linalg.norm(point2 - point1)
                    # )
                    collision_distances.append(collision_distance)
                distance = min(collision_distances) - self.size[0] * 0.5 - 1
                distances.append(distance)
            else:
                distances.append(-1)

        return distances

    # def generate_sprite(self, colour):
    #     return super().generate_sprite(colour)

    def debug_draw(self, screen):
        super().debug_draw(screen)
        for line in self.distance_lines:
            line.debug_draw(screen, (255, 125, 20))


def add_vectors(vector_a, vector_b):
    def _Point(vector_a, vector_b):
        return [
            vector_a[0] + vector_b[0],
            vector_a[1] + vector_b[1]
        ]

    if isinstance(vector_a, list):
        if isinstance(vector_a[0], list):
            raise NotImplementedError()
            # Is Line
        else:
            # Is Point
            return _Point(vector_a, vector_b)
