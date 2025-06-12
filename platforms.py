import pygame

class Platform:
    def __init__(self, x, y, width=120, height=20):
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.x -= speed  # scroll left

    def draw(self, screen):
        screen.blit(self.image, self.rect)
