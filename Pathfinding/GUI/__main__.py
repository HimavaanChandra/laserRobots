"""Main Program, entry point"""
import sys
import pygame

from window import Window
from grid import Grid


# Fix for pygame Init import
# pylint: disable=no-member

if __name__ == '__main__':
    WINDOW = Window(300, 200)
    GRID = Grid(WINDOW)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        GRID.convert()
        GRID.draw()
