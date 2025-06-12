import pygame
from settings import WIDTH, HEIGHT, BG_COLOR
from platforms import Platform
from player import Player
from level import Level

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = Player()
level = Level()

running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time for consistent movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(level.platforms)
    level.update()

    screen.fill(BG_COLOR)
    level.draw(screen)
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
