"""Window Class"""
import pygame


class Window():
    """Window handles the low level pygame implementation"""
    fps = 10
    grid_size = 4

    def __init__(self, width, height):
        self.screen_size(width, height)

        pygame.init()
        pygame.key.set_repeat(1, 40)
        self.fps_clock = pygame.time.Clock()
        self.clock = pygame.time.Clock()

        self.display()

    def screen_size(self, width, height):
        """Determine screen size based on grid dimensions"""
        self.grid_width = width
        self.grid_height = height

        self.screen_width = self.grid_width * self.grid_size
        self.screen_height = self.grid_height * self.grid_size

    def display(self):
        """Setup pygame display"""
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            0,
            32
        )

        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((255, 255, 255))
        self.screen.blit(self.surface, (0, 0))

    def tick(self, delay=0):
        """Increment game tick"""
        self.fps_clock.tick(self.fps + delay)

    @staticmethod
    def draw_box(surf, color, pos):
        """Draw a rectangle to the game surface"""
        coordinates = (pos[0] * Window.grid_size, pos[1] * Window.grid_size)
        size = (Window.grid_size, Window.grid_size)
        rectangle = pygame.Rect(coordinates, size)
        pygame.draw.rect(surf, color, rectangle)
