"""Main Program, entry point"""
import sys
import pygame

from window import Window
from grid import Grid


# Fix for pygame Init import
# pylint: disable=no-member

if __name__ == '__main__':
    WINDOW = Window(12, 8)
    GRID = Grid(WINDOW)
    mouse_click = False
    mouse_button = None
    GRID.draw()
    EXPORT_FILENAME = "filename"

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_click = False

            elif event.type == pygame.MOUSEMOTION:
                if mouse_click:
                    mouse_button = pygame.mouse.get_pressed()
                    if mouse_button[0] == 1:
                        pos = pygame.mouse.get_pos()
                        # print("Mouse click: ", pos)
                        grid_position = GRID.pixle_grid_position(pos)
                        lg_grid_position = GRID.lg_grid(grid_position)
                        # print("Cell position: ", grid_position)
                        GRID.lg_convert(lg_grid_position)
                        # GRID.convert(grid_position)
                    if mouse_button[2] == 1:
                        pos = pygame.mouse.get_pos()
                        # print("Mouse click: ", pos)
                        grid_position = GRID.pixle_grid_position(pos)
                        lg_grid_position = GRID.lg_grid(grid_position)
                        # print("Cell position: ", grid_position)
                        GRID.lg_remove(lg_grid_position)
                        # GRID.convert(grid_position)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    GRID.import_csv(EXPORT_FILENAME)
                    print("imported: " + EXPORT_FILENAME)
                elif event.key == pygame.K_e:
                    GRID.export_csv(EXPORT_FILENAME)
                    print("exported: " + EXPORT_FILENAME)

        GRID.draw()
        # GRID.convert()
