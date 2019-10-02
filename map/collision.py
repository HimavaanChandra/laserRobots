# from entity import Square, Line, Point
from config import DEBUG


class Collision():
    """Class to hold all the collision types"""
    line_collisions = []

    @staticmethod
    def point_point(point1, point2):
        """Points are equal"""
        return point1.vector[0] == point2.vector[0] and point1.vector[1] == point2.vector[1]

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
        p = line1.origin
        r = line1.size
        q = line2.origin
        s = line2.size

        q_minus_p = [
            q[0] - p[0],
            q[1] - q[1]
        ]

        numerator = q_minus_p[0] * s[1] - q_minus_p[1] * s[0]
        denominator = r[0] * s[1] - r[1] * s[0]

        if numerator == 0 and denominator == 0:
            # lines are collinear
            # t0 = np.divide(
            #     np.dot(np.subtract(q, p), r),
            #     np.dot(r, r)
            # )
            # t1 = np.add(t0, np.divide(
            #     np.dot(s, r),
            #     np.dot(r, r)
            # ))
            # print("[%f, %f]" % (t0, t1))

            # lines maybe intersect
            return False
        elif numerator != 0 and denominator == 0:
            # lines are parallel
            # lines do not intersect
            return False
        else:
            # lines are not parallel
            u = numerator / denominator
            t = (q_minus_p[0] * r[1] - q_minus_p[1] * r[0]) / denominator

            if (0 <= t <= 1) and (0 <= u <= 1):
                # lines intersect
                return True
            else:
                # lines do not intersect
                return False

    @staticmethod
    def line_square(line, square):
        """Test if line intersects any of the square lines"""
        collisions = []
        for square_line in square.lines:
            if Collision.line_line(line, square_line) is True:
                Collision.line_collisions.append(line)
                Collision.line_collisions.append(square_line)
                collisions.append(square_line)
        if not collisions:
            return False
        else:
            return collisions

    @staticmethod
    def square_square(square1, square2):
        """Test if any of the square lines intersect"""
        collisions = []
        for square_line1 in square1.lines:
            for square_line2 in square2.lines:
                if Collision.line_line(square_line1, square_line2) is True:
                    Collision.line_collisions.append(square_line1)
                    Collision.line_collisions.append(square_line2)
                    collisions.append(square_line2)
        if not collisions:
            return False
        else:
            return collisions

    @staticmethod
    def debug_draw(screen):
        if DEBUG is True:
            for line in Collision.line_collisions:
                line.debug_draw(screen, (255, 0, 0))
