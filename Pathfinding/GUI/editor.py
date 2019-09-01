import pygame
import sys
import time
import random

from pygame.locals import *

# Fix for pygame Init import
# pylint: disable=no-member


class Window():
    fps = 10
    gridSize = 10

    def __init__(self, width, height):
        self.screenSize(width, height)

        pygame.init()
        pygame.key.set_repeat(1, 40)
        self.fpsClock = pygame.time.Clock()
        self.clock = pygame.time.Clock()

        self.display()

    def screenSize(self, width, height):
        self.gridWidth = width
        self.gridHeight = height

        self.screenWidth = self.gridWidth * self.gridSize
        self.screenHeight = self.gridHeight * self.gridSize

    def display(self):
        self.screen = pygame.display.set_mode(
            (self.screenWidth, self.screenHeight),
            0,
            32
        )

        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((255, 255, 255))
        self.screen.blit(self.surface, (0, 0))

    def tick(self, delay=0):
        self.fpsClock.tick(self.fps + delay)


def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0] * Window.gridSize, pos[1] *
                     Window.gridSize), (Window.gridSize, Window.gridSize))
    pygame.draw.rect(surf, color, r)


class Map(object):
    def __init__(self, window):
        self.cells = []
        self.window = window
        self.size = (self.window.gridWidth, self.window.gridHeight)
        self.generateCells()

    def generateCells(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.addCell(x, y)

    def addCell(self, x, y):
        cell = Cell(self, x, y)
        self.cells.append(cell)

    def draw(self):
        self.window.surface.fill((255, 255, 255))
        for cell in self.cells:
            cell.draw(self.window.surface)

        self.window.screen.blit(self.window.surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        self.window.tick()

    def convert(self):
        index = random.randint(0, len(self.cells) - 1)
        cell = self.cells[index]
        cell = Wall(cell.map, cell.position[0], cell.position[1])
        self.cells[index] = cell


class Cell:
    def __init__(self, map, x, y):
        self.map = map
        self.position = (x, y)
        self.colour = (255, 0, 0)

    def draw(self, surf):
        draw_box(surf, self.colour, self.position)


class Wall(Cell):
    def __init__(self, map, x, y):
        super().__init__(map, x, y)
        self.colour = (0, 0, 0)
        self.randomize()

    def randomize(self):
        self.position = (
            random.randint(0, self.map.size[0] - 1),
            random.randint(0, self.map.size[1] - 1)
        )


if __name__ == '__main__':
    window = Window(20, 20)
    map = Map(window)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        map.convert()
        map.draw()
