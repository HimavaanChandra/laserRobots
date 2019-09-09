"""Cell class and sub classes"""
import random

from window import Window


class Cell:
    """Generic Cell class. Used for empty spaces in grid."""

    def __init__(self, grid, x, y):
        self.grid = grid
        self.position = (x, y)
        self.colour = (255, 0, 0)

    def draw(self, surf):
        """Called to paint the cell to the window"""
        Window.draw_box(surf, self.colour, self.position)


class Wall(Cell):
    """Wall class cannot be passed through."""

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)
        self.colour = (0, 0, 0)
        self.randomize()

    def randomize(self):
        """Randomly relocate to a new position."""
        self.position = (
            random.randint(0, self.grid.size[0] - 1),
            random.randint(0, self.grid.size[1] - 1)
        )
