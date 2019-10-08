#!/usr/bin/env python3
import pygame

from .collision import Collision
from .config import DEBUG


class SimEntity():
    def __init__(self, vector):
        self.vector = vector

    def move(self, m_vector):
        pass

    def update(self):
        pass

    def debug_draw(self, screen, colour):
        pass

    def __str__(self):
        pass


class Point(SimEntity):
    def __init__(self, x=0, y=0, vector=None):
        # pylint: disable=invalid-name
        if vector is None:
            vector = [x, y]
        else:
            x = vector[0]
            y = vector[1]
        self.x = x
        self.y = y
        super().__init__(vector)

    def move(self, m_vector):
        self.x += m_vector[0]
        self.y += m_vector[1]
        self.update()

    def set(self, s_vector):
        self.x = s_vector[0]
        self.y = s_vector[1]
        self.update()

    def update(self):
        self.vector = [
            self.x,
            self.y
        ]

    def debug_draw(self, screen, colour):
        if DEBUG is True:
            point = self.vector
            pygame.draw.circle(screen, colour, point, 4)

    def __str__(self):
        point = self.vector
        return str(point)


class Line(SimEntity):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        vector = [
            self.start,
            self.end
        ]
        self.size = []
        self.origin = []

        super().__init__(vector)
        self.update()

    def update(self):
        self.vector = [
            self.start.vector,
            self.end.vector
        ]
        self.size = [
            self.vector[1][0] - self.vector[0][0],
            self.vector[1][1] - self.vector[0][1]
        ]
        self.origin = [
            self.vector[0][0],
            self.vector[0][1]
        ]

    def move(self, m_vector):
        self.start.move(m_vector)
        self.end.move(m_vector)
        self.update()

    def set(self, s_vector):
        origin = s_vector
        size = [
            s_vector[0] + self.size[0],
            s_vector[1] + self.size[1]
        ]

        self.start.set(origin)
        self.end.set(size)
        self.update()

    def debug_draw(self, screen, colour):
        if DEBUG is True:
            start = self.vector[0]
            end = self.vector[1]
            pygame.draw.line(screen, colour, start, end, 4)

    def __str__(self):
        start = self.vector[0]
        end = self.vector[1]
        return str(start) + ", " + str(end)


class Square(SimEntity):
    """2D square composed of 4 lines"""

    def __init__(self, point1=None, point2=None):
        self.sprite = None
        self.lines = []
        self.points = []
        self.size = [0, 0]
        self.origin = [0, 0]
        self.center = [0, 0]
        self.bottom_left = [0, 0]
        self.bottom_right = [0, 0]
        self.top_left = [0, 0]
        self.top_right = [0, 0]
        self._generate_lines(point1, point2)
        self.update()
        # super().__init__([

        # ])

    def _generate_lines(self, point1, point2):
        """Populates the line list based on the square corners"""
        # Create a cross inside the rectagle to find the corner points
        diagonal = Line(start=point1, end=point2)

        # Set up the corner points
        self.bottom_left = Point(diagonal.vector[0][0], diagonal.vector[0][1])
        self.bottom_right = Point(diagonal.vector[0][0], diagonal.vector[1][1])
        self.top_left = Point(diagonal.vector[1][0], diagonal.vector[0][1])
        self.top_right = Point(diagonal.vector[1][0], diagonal.vector[1][1])

        # Create the lines for the square
        self.lines.clear()
        self.lines.append(Line(
            start=self.bottom_left,
            end=self.top_left
        ))
        self.lines.append(Line(
            start=self.top_left,
            end=self.top_right
        ))
        self.lines.append(Line(
            start=self.top_right,
            end=self.bottom_right
        ))
        self.lines.append(Line(
            start=self.bottom_right,
            end=self.bottom_left
        ))

        self.points.append(self.bottom_left)
        self.points.append(self.bottom_right)
        self.points.append(self.top_right)
        self.points.append(self.top_left)

    def update(self):
        self.size = [
            self.top_right.vector[0] - self.bottom_left.vector[0],
            self.top_right.vector[1] - self.bottom_left.vector[1]
        ]
        self.origin = [
            self.bottom_left.vector[0],
            self.bottom_left.vector[1]
        ]
        self.center = [
            self.origin[0] + self.size[0] * 0.5,
            self.origin[1] + self.size[1] * 0.5
        ]
        for line in self.lines:
            line.update()

    def move(self, m_vector):
        for point in self.points:
            # Only move single point for squares since lines share points.
            point.move(m_vector)
        self.update()

    def set(self, s_vector):
        origin = Point(vector=s_vector)
        size = Point(vector=[
            s_vector[0] + self.size[0],
            s_vector[1] + self.size[1]
        ])
        self._generate_lines(origin, size)
        # for line in self.lines:
        #     # Only set single point for squares since lines share points.
        #     line.set(s_vector)
        self.update()

    def check_line_collision(self, test_line):
        """Check if the test line intersects any of the square lines"""
        return Collision.line_square(test_line, self)

    def check_square_collision(self, test_square):
        """Check if the test square intersects any of the square lines"""
        return Collision.square_square(test_square, self)

    def generate_sprite(self, colour):
        # Make a BLUE, of the size specified in the parameters
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface(self.size)
        sprite.image.fill(colour)

        # Make our top-left corner the passed-in location.
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = self.origin[0]
        sprite.rect.y = self.origin[1]

        return sprite

    def debug_draw(self, screen):
        if DEBUG is True:
            for line in self.lines:
                line.debug_draw(screen, (0, 255, 0))

    def __str__(self):
        string = ""
        for line in self.lines:
            string += str(line) + " : "
        return string
