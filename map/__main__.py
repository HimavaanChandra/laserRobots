import numpy as np


def load_grid(filename="filename"):
    grid_csv = np.loadtxt(filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list


class Point():
    def __init__(self, x=0, y=0):
        # pylint: disable=invalid-name
        self.vector = np.array([x, y])


class Line():
    def __init__(self, x1=0, y1=0, x2=0, y2=0, p1=None, p2=None):
        if p1 is None and p2 is None:
            self.p1 = Point(x1, y1)
            self.p2 = Point(x2, y2)
        else:
            self.p1 = p1
            self.p2 = p2
        self.vector = np.array([self.p1.vector, self.p2.vector])

    def distance(self):
        return np.subtract(self.p2.vector, self.p1.vector)

    def origin(self):
        return self.p1.vector


def check_intersection(line1, line2):
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


class Square():
    def __init__(self, x1=0, y1=0, x2=1, y2=1):
        # pylint: disable=invalid-name
        self.points = []
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def _generate_points(self):
        self.points.clear()
        self.points.append(Point(self.x1, self.y1))
        self.points.append(Point(self.x1, self.y2))
        self.points.append(Point(self.x2, self.y1))
        self.points.append(Point(self.x2, self.y2))

    def check_x(self, x_line):
        point_check = 0
        for point in self.points:
            if x_line > point.x:
                point_check += 1
            else:
                point_check += 0
        if point_check < len(self.points) and point_check > 0:
            return True
        else:
            return False


def Main():
    line1 = Line(0, 0, 2, 4)
    line2 = Line(1, 2, 4, 8)

    print(check_intersection(line1, line2))


if __name__ == '__main__':
    Main()
