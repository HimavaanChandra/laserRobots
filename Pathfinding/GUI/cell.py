"""Cell class and sub classes"""
import random
import enum
from window import Window


class CellTypes(enum.Enum):
    """Enum of cell types"""
    empty = 0
    wall = 1


class Cell:
    """Generic Cell class. Used for empty spaces in grid."""
    cell_type = CellTypes.empty

    def __init__(self, grid, x, y):
        self.grid = grid
        self.position = (x, y)
        self.colour = (255, 0, 0)

    def draw(self, surf):
        """Called to paint the cell to the window"""
        if self.cell_type != CellTypes.empty:
            Window.draw_box(surf, self.colour, self.position)

    def get_type(self):
        """returns cell enum type"""
        return self.cell_type.value


class Wall(Cell):
    """Wall class cannot be passed through."""
    cell_type = CellTypes.wall

    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)
        self.colour = (0, 0, 0)
        # self.randomize()

    def randomize(self):
        """Randomly relocate to a new position."""
        self.position = (
            random.randint(0, self.grid.size[0] - 1),
            random.randint(0, self.grid.size[1] - 1)
        )
