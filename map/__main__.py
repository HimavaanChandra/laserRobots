import numpy as np
import pygame as pygame

from simlayer import SimLayer
from game import add_vectors
from collision import Collision
from config import SCREEN, SCALE


def load_grid(filename="filename"):
    grid_csv = np.loadtxt(filename + ".csv", delimiter=',')
    grid_list = np.array(grid_csv).tolist()
    return grid_list


def main():
    grid = load_grid()

    global SCREEN
    screen = pygame.display.set_mode([len(grid[0]) * SCALE, len(grid) * SCALE])
    SCREEN = screen

    sim = SimLayer(grid)

    test = sim.spawn_instance("Test")
    test.spawn_robots(0, 0, 300, 300)

    pygame.display.set_caption('MAP Sim')
    clock = pygame.time.Clock()

    done = False
    m_vector = [0, 0]
    m_speed = 5
    m_unit = 1
    while done is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    break
                if event.key == pygame.K_r:
                    Collision.line_collisions.clear()
                    test.set(0, [100, 100])
                if event.key == pygame.K_LEFT:
                    m_vector = add_vectors(m_vector, [-m_unit, 0])
                if event.key == pygame.K_RIGHT:
                    m_vector = add_vectors(m_vector, [m_unit, 0])
                if event.key == pygame.K_UP:
                    m_vector = add_vectors(m_vector, [0, -m_unit])
                if event.key == pygame.K_DOWN:
                    m_vector = add_vectors(m_vector, [0, m_unit])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    m_vector = add_vectors(m_vector, [m_unit, 0])
                if event.key == pygame.K_RIGHT:
                    m_vector = add_vectors(m_vector, [-m_unit, 0])
                if event.key == pygame.K_UP:
                    m_vector = add_vectors(m_vector, [0, m_unit])
                if event.key == pygame.K_DOWN:
                    m_vector = add_vectors(m_vector, [0, -m_unit])

        for _ in range(m_speed):
            test.move(0, m_vector)

        # --- Drawing ---
        screen.fill((0, 0, 0))
        test.debug_draw(screen)
        print(test.data(0))
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
