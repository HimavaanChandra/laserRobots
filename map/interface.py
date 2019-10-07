import numpy as np
import pygame as pygame

from simlayer import SimLayer
from config import SCALE


def load_grid(filename="filename"):
    grid_csv = np.loadtxt(filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list


def main():
    grid = load_grid()

    screen = pygame.display.set_mode([len(grid[0]) * SCALE, len(grid) * SCALE])

    sim = SimLayer(grid)

    tests = []

    for i in range(0, 10):
        test = sim.spawn_instance("Test " + str(i))
        test.spawn_robots(0, 0, 300, 300)
        tests.append(test)

    pygame.display.set_caption('MAP Sim')
    clock = pygame.time.Clock()

    done = False
    m_unit = 1
    while not done:
        instance = input("Enter instance: ")
        robot = input("Enter robot: ")
        x = input("Enter movement x: ")
        y = input("Enter movement y: ")

        try:
            instance = int(instance)
            robot = int(robot)
            x = int(x)
            y = int(y)
        except ValueError:
            print("Bad input!")
            continue

        if len(tests) > instance:
            test = tests[instance]
        else:
            print("Bad input!")
            continue

        test.move(robot, [int(x) * m_unit, int(y) * m_unit])

        # --- Drawing ---
        screen.fill((0, 0, 0))
        test.debug_draw(screen)
        print(test.data(robot))
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
