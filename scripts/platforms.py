import pygame

class Platform:
    def __init__(self, x, y, width, height, color=(60, 60, 60)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)