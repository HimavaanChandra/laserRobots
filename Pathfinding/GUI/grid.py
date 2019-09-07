"""Grid Class"""
import random
import pygame

from cell import Cell, Wall


class Grid():
    """Grid class holds and manipulates all the cells in the window."""

    def __init__(self, window):
        self.cells = []
        self.window = window
        self.size = (self.window.grid_width, self.window.grid_height)
        self.generate_cells()

    def generate_cells(self):
        """Populate the grid with cells"""
        for y_position in range(self.size[1]):
            for x_position in range(self.size[0]):
                self.add_cell(x_position, y_position)

    def add_cell(self, x_position, y_position):
        """Create a cell"""
        cell = Cell(self, x_position, y_position)
        self.cells.append(cell)

    def draw(self):
        """Called to paint the cells to the window"""
        self.window.surface.fill((255, 255, 255))
        for cell in self.cells:
            cell.draw(self.window.surface)

        self.window.screen.blit(self.window.surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        self.window.tick()

    def convert(self):
        """Randomly convert existing cells into walls"""
        index = random.randint(0, len(self.cells) - 1)
        cell = self.cells[index]
        cell = Wall(cell.grid, cell.position[0], cell.position[1])
        self.cells[index] = cell
