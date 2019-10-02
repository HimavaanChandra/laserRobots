import numpy as np
import pygame as pygame
import math
import time

from entity import Square, Line, Point
from collision import Collision
from config import SIZE, DEBUG, SCREEN


def load_grid(filename="filename"):
    grid_csv = np.loadtxt(filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list


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
        right = self._generate_distance_line(center, [0, -length])
        up = self._generate_distance_line(center, [length, 0])
        down = self._generate_distance_line(center, [-length, 0])

        self.distance_lines.clear()
        self.distance_lines.append(left)
        self.distance_lines.append(right)
        self.distance_lines.append(up)
        self.distance_lines.append(down)

    def move(self, vector, wall_container):
        super().move(vector)

        if Collision.square_square(wall_container.container, self):
            super().move([
                - vector[0],
                - vector[1]
            ])
        elif wall_container.check_square_collision(self) is not False:
            super().move([
                - vector[0],
                - vector[1]
            ])
        else:
            # No Collisions
            self.update()
            # Move Distance Lines
            for line in self.distance_lines:
                line.move(vector)

    def update(self):
        super().update()
        if self.sprite is not None:
            # Move Sprite Rectangle
            self.sprite.rect.x = self.origin[0]
            self.sprite.rect.y = self.origin[1]

    def distance(self, wall_container):
        origin = self.origin
        distances = []

        for line in self.distance_lines:
            result = wall_container.check_line_collision(line)
            if result is not False:
                collision_distances = []
                for collision in result:
                    point1 = collision.start.vector
                    point2 = collision.end.vector

                    a = point2[0] - point1[0]
                    b = point2[1] - point1[1]

                    numerator = a * origin[0] - b * origin[1]
                    denominator = math.sqrt((a)**2 + (b)**2)

                    collision_distance = numerator / denominator

                    # collision_distance = np.divide(
                    #     np.abs(np.cross(
                    #         point2 - point1,
                    #         point1 - origin
                    #     )),
                    #     np.linalg.norm(point2 - point1)
                    # )
                    collision_distances.append(collision_distance)
                distance = min(collision_distances) - self.size[0] * 0.5
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

    


def main():
    size = SIZE
    grid = load_grid()
    walls = WallContainer(len(grid[0]) * size, len(grid) * size)

    global SCREEN
    screen = pygame.display.set_mode([len(grid[0]) * size, len(grid) * size])
    SCREEN = screen

    for row_i in range(0, len(grid)):
        for cell_i in range(0, len(grid[row_i])):
            cell = grid[row_i][cell_i]
            if cell == 1:
                y_1 = row_i * size
                y_2 = y_1 + size
                x_1 = cell_i * size
                x_2 = x_1 + size

                walls.add(Wall(x_1, y_1, x_2, y_2))

    robots = pygame.sprite.Group()

    robot1 = Robot(200, 400, 200 + size - 6, 400 + size - 6)
    robots.add(robot1.sprite)

    pygame.display.set_caption('MAP Sim')
    clock = pygame.time.Clock()

    done = False
    m_vector = [0, 0]
    m_speed = 1
    m_unit = 1
    while done is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    break
                if event.key == pygame.K_r:
                    Collision.line_collisions.clear()
                if event.key == pygame.K_LEFT:
                    m_vector = add_vectors(m_vector, [-m_unit, 0])
                if event.key == pygame.K_RIGHT:
                    m_vector = add_vectors(m_vector, [m_unit, 0])
                if event.key == pygame.K_UP:
                    m_vector = add_vectors(m_vector, [0, -m_unit])
                if event.key == pygame.K_DOWN:
                    m_vector = add_vectors(m_vector, [0, m_unit])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    m_vector = add_vectors(m_vector, [m_unit, 0])
                if event.key == pygame.K_RIGHT:
                    m_vector = add_vectors(m_vector, [-m_unit, 0])
                if event.key == pygame.K_UP:
                    m_vector = add_vectors(m_vector, [0, m_unit])
                if event.key == pygame.K_DOWN:
                    m_vector = add_vectors(m_vector, [0, -m_unit])

        for i in range(0, m_speed):
            robot1.move(m_vector, walls)
        print(robot1.distance(walls))

        # --- Drawing ---
        screen.fill((0, 0, 0))

        walls.wall_sprites.draw(screen)
        walls.debug_draw(screen)
        robot1.debug_draw(screen)
        Collision.debug_draw(screen)
        # robot1.move(np.array([5, 0]), walls)
        robots.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
