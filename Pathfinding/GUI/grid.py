"""Grid Class"""
# import random
import pygame
import numpy

from cell import Cell, Wall


class Grid():
    """Grid class holds and manipulates all the cells in the window."""
    lg_grid_size = 1

    def __init__(self, window):
        self.cells = []
        self.window = window
        self.size = (self.window.grid_width, self.window.grid_height)
        self.generate_cells()
        self.window.surface.fill((255, 255, 255))
        self.updated = True

    def generate_cells(self):
        """Populate the grid with cells"""
        for y_position in range(0, self.size[1]):
            row = []
            for x_position in range(0, self.size[0]):
                # self.add_cell(x_position, y_position)
                cell = Cell(self, x_position, y_position)
                row.append(cell)
            self.cells.append(row)

    def add_cell(self, x_position, y_position):
        """Create a cell"""
        cell = Cell(self, x_position, y_position)
        self.cells.append(cell)

    def draw(self):
        """Called to paint the cells to the window"""
        if self.updated is True:
            for row in self.cells:
                for cell in row:
                    cell.draw(self.window.surface)

            self.window.screen.blit(self.window.surface, (0, 0))
            pygame.display.flip()
            pygame.display.update()
            self.window.tick()

    def pixle_grid_position(self, pixle_position):
        """Determine grid position from pixle position"""
        x_position = int(pixle_position[0] / self.window.grid_size)
        y_position = int(pixle_position[1] / self.window.grid_size)

        return (x_position, y_position)

    def lg_grid(self, position):
        lg_x = int(position[0] / self.lg_grid_size)
        lg_y = int(position[1] / self.lg_grid_size)
        return (lg_x, lg_y)

    def lg_convert(self, position):
        self.updated = True
        x_start = position[0] * self.lg_grid_size
        x_end = (position[0]+1) * self.lg_grid_size
        x_range = range(x_start, x_end)
        y_start = position[1] * self.lg_grid_size
        y_end = (position[1]+1) * self.lg_grid_size
        y_range = range(y_start, y_end)

        for row_index in y_range:
            for cell_index in x_range:
                cell = self.cells[row_index][cell_index]
                cell = Wall(cell.grid, cell.position[0], cell.position[1])
                self.cells[row_index][cell_index] = cell

    def lg_remove(self, position):
        self.updated = True
        x_start = position[0] * self.lg_grid_size
        x_end = (position[0]+1) * self.lg_grid_size
        x_range = range(x_start, x_end)
        y_start = position[1] * self.lg_grid_size
        y_end = (position[1]+1) * self.lg_grid_size
        y_range = range(y_start, y_end)

        for row_index in y_range:
            for cell_index in x_range:
                cell = self.cells[row_index][cell_index]
                cell = Cell(cell.grid, cell.position[0], cell.position[1])
                self.cells[row_index][cell_index] = cell

    def convert(self, position):
        """Randomly convert existing cells into walls"""
        # row_index = random.randint(0, len(self.cells) - 1)
        # cell_index = random.randint(0, len(self.cells[row_index]) - 1)
        row_index = position[1]
        cell_index = position[0]

        cell = self.cells[row_index][cell_index]

        cell = Wall(cell.grid, cell.position[0], cell.position[1])
        self.cells[row_index][cell_index] = cell

    def import_csv(self, filename):
        self.updated = True
        """Export cells as a csv"""
        cell_map = numpy.loadtxt(filename + ".csv", delimiter=',')
        cell_array = numpy.array(cell_map).tolist()
        self.cells.clear()
        for y_position in range(len(cell_array)):
            row = []
            for x_position in range(len(cell_array[y_position])):
                # self.add_cell(x_position, y_position)
                if cell_array[y_position][x_position] == 1:
                    wall = Wall(self, x_position, y_position)
                    row.append(wall)
                else:
                    cell = Cell(self, x_position, y_position)
                    row.append(cell)
            self.cells.append(row)

    def export_csv(self, filename):
        """Export cells as a csv"""
        cell_map = [[cell.get_type() for cell in row] for row in self.cells]

        # for row in self.cells:
        #     for cell in row:
        #         cell.get_type

        # cell_array = numpy.array(list(cell_map))
        numpy.savetxt(filename + ".csv", cell_map,
                      delimiter=",", fmt='%i')
