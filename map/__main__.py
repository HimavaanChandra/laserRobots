import numpy as np
import pygame as pygame


def load_grid(filename="filename"):
    grid_csv = np.loadtxt(filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list


class SimEntity():
    def __init__(self, vector):
        self.vector = vector

    def move(self, m_vector):
        self.vector = np.add(self.vector, m_vector)

    def update(self):
        pass

    def debug_draw(self, screen, colour):
        point = self.vector[0, :].tolist()
        pygame.draw.circle(screen, colour, point, 4)

    def __str__(self):
        point = self.vector[0, :].tolist()
        return str(point)


class Point(SimEntity):
    def __init__(self, x=0, y=0, vector=None):
        # pylint: disable=invalid-name
        if vector is None:
            vector = np.array([x, y])
        else:
            vector = vector
        super().__init__(vector)


class Line():
    def __init__(self, point1=None, point2=None):
        self.point1 = point1
        self.point2 = point2
        self.update()

    def update(self):
        self.vector = np.array([self.point1.vector, self.point2.vector])

    def distance(self):
        return np.subtract(self.point2.vector, self.point1.vector)

    def origin(self):
        return self.point1.vector

    def move(self, m_vector):
        self.point1.move(m_vector)
        self.point2.move(m_vector)
        self.update()

    def debug_draw(self, screen, colour):
        start = self.vector[0, :].tolist()
        end = self.vector[1, :].tolist()
        pygame.draw.line(screen, colour, start, end, 4)

    def __str__(self):
        start = self.vector[0, :].tolist()
        end = self.vector[1, :].tolist()
        return str(start) + ", " + str(end)

    @staticmethod
    def rotate90(line):
        new_vector = np.rot90(line.vector)
        point1 = Point(vector=new_vector[0, :])
        point2 = Point(vector=new_vector[1, :])
        return Line(point1=point1, point2=point2)


class Collision():
    """Class to hold all the collision types"""
    @staticmethod
    def point_point(point1, point2):
        """Points are equal"""
        return point1.vector == point2.vector

    @staticmethod
    def point_line(point, line):
        """point to line collision method"""
        raise NotImplementedError()

    @staticmethod
    def line_line(line1, line2):
        """line to line collision method"""
        # Stolen from
        # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
        # pylint: disable=invalid-name
        p = line1.origin()
        r = line1.distance()
        q = line2.origin()
        s = line2.distance()

        numerator = np.cross(np.subtract(q, p), s)
        denominator = np.cross(r, s)

        # print(numerator)
        # print("------------")
        # print(denominator)

        if numerator == 0 and denominator == 0:
            # lines are collinear
            t0 = np.divide(
                np.dot(np.subtract(q, p), r),
                np.dot(r, r)
            )
            t1 = np.add(t0, np.divide(
                np.dot(s, r),
                np.dot(r, r)
            ))
            # print("[%f, %f]" % (t0, t1))

            # lines maybe intersect
            return False
        elif numerator != 0 and denominator == 0:
            # lines are parallel
            # lines do not intersect
            return False
        else:
            # lines are not parallel
            u = np.divide(numerator, denominator)
            t = np.divide(
                np.cross(np.subtract(q, p), r),
                denominator
            )
            if (0 <= t <= 1) and (0 <= u <= 1):
                # lines intersect
                return True
            else:
                # lines do not intersect
                return False

    @staticmethod
    def line_square(line, square):
        """Test if line intersects any of the square lines"""
        for square_line in square.lines:
            if Collision.line_line(line, square_line) is True:
                return True
        return False

    @staticmethod
    def square_square(square1, square2):
        """Test if any of the square lines intersect"""
        for square_line1 in square1.lines:
            for square_line2 in square2.lines:
                if Collision.line_line(square_line1, square_line2) is True:
                    sl1_s = square_line1.vector[0, :].tolist()
                    sl1_e = square_line1.vector[1, :].tolist()
                    sl2_s = square_line2.vector[0, :].tolist()
                    sl2_e = square_line2.vector[1, :].tolist()
                    pygame.draw.line(SCREEN, (255, 0, 0), sl1_s, sl1_e, 4)
                    pygame.draw.line(SCREEN, (255, 0, 0), sl2_s, sl2_e, 4)
                    return True
        return False


class Square():
    """2D square composed of 4 lines"""
    def __init__(self, point1=None, point2=None):
        self.lines = []
        self.size = None
        self.origin = None
        self._generate_lines(point1, point2)

    def _generate_lines(self, point1, point2):
        """Populates the line list based on the square corners"""
        # Create a cross inside the rectagle to find the corner points
        diagonal = Line(point1=point1, point2=point2)
        self.size = diagonal.distance()
        self.origin = diagonal.origin()

        # Set up the corner points
        bottom_left = diagonal.point1
        bottom_right = Point(diagonal.point1.vector[0], diagonal.point2.vector[1])
        top_left = Point(diagonal.point2.vector[0], diagonal.point1.vector[1])
        top_right = diagonal.point2

        # Create the lines for the square
        self.lines.clear()
        self.lines.append(Line(
            point1=bottom_left,
            point2=top_left
        ))
        self.lines.append(Line(
            point1=top_left,
            point2=top_right
        ))
        self.lines.append(Line(
            point1=top_right,
            point2=bottom_right
        ))
        self.lines.append(Line(
            point1=bottom_right,
            point2=bottom_left
        ))

    def update(self):
        pass

    def move(self, m_vector):
        for line in self.lines:
            # Only move single point for squares since lines share points.
            line.point1.move(m_vector)
        for line in self.lines:

            line.update()
        self.origin = np.add(self.origin, m_vector)

    def check_line_collision(self, test_line):
        """Check if the test line intersects any of the square lines"""
        return Collision.line_square(test_line, self)

    def check_square_collision(self, test_square):
        """Check if the test square intersects any of the square lines"""
        return Collision.square_square(test_square, self)

    def generate_sprite(self, colour):
        # Make a BLUE, of the size specified in the parameters
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface(self.size.tolist())
        sprite.image.fill(colour)

        # Make our top-left corner the passed-in location.
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = self.origin[0]
        sprite.rect.y = self.origin[1]

        return sprite

    def debug_draw(self, screen):
        for line in self.lines:
            line.debug_draw(screen, (0, 255, 0))

    def __str__(self):
        string = ""
        for line in self.lines:
            string += str(line) + " : "
        return string


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
            if result is True:
                collisions.append(wall)
        if collisions is None:
            return False
        else:
            return collisions

    def check_square_collision(self, test_square):
        collisions = []
        for wall in self.walls:
            result = wall.check_square_collision(test_square)
            if result is True:
                collisions.append(wall)
        if not collisions:
            return False
        else:
            return collisions

    def debug_draw(self, screen):
        for wall in self.walls:
            wall.debug_draw(screen)
            # print("Wall: " + str(wall))


class Robot(Square):
    def __init__(self, x_1, y_1, x_2, y_2, point1=None, point2=None):
        if point1 is None and point2 is None:
            point1 = Point(x_1, y_1)
            point2 = Point(x_2, y_2)

        super().__init__(point1, point2)
        self.sprite = self.generate_sprite((0, 125, 125))

    def move(self, vector, wall_container):
        super().move(vector)
        if Collision.square_square(wall_container.container, self):
            super().move(np.negative(vector))
        if wall_container.check_square_collision(self) is not False:
            super().move(np.negative(vector))
        else:
            self.sprite.rect.x = self.origin[0]
            self.sprite.rect.y = self.origin[1]    

    def distance(self):
        pass


SIZE = 100
SCREEN = None

def Main():
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

    robot1 = Robot(0, 0, size - 2, size - 2)
    robots.add(robot1.sprite)

    pygame.display.set_caption('MAP Sim')
    clock = pygame.time.Clock()

    done = False
    m_vector = np.array([0, 0])
    speed = 10
    while done is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    m_vector = np.add(m_vector, np.array([-speed, 0]))
                if event.key == pygame.K_RIGHT:
                    m_vector = np.add(m_vector, np.array([speed, 0]))
                if event.key == pygame.K_UP:
                    m_vector = np.add(m_vector, np.array([0, -speed]))
                if event.key == pygame.K_DOWN:
                    m_vector = np.add(m_vector, np.array([0, speed]))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    m_vector = np.subtract(m_vector, np.array([-speed, 0]))
                if event.key == pygame.K_RIGHT:
                    m_vector = np.subtract(m_vector, np.array([speed, 0]))
                if event.key == pygame.K_UP:
                    m_vector = np.subtract(m_vector, np.array([0, -speed]))
                if event.key == pygame.K_DOWN:
                    m_vector = np.subtract(m_vector, np.array([0, speed]))


        robot1.move(m_vector, walls)
            
        # --- Drawing ---
        screen.fill((0, 0, 0))

        walls.wall_sprites.draw(screen)
        walls.debug_draw(screen)
        robot1.debug_draw(screen)
        # robot1.move(np.array([5, 0]), walls)
        # robots.draw(screen)

        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    Main()
