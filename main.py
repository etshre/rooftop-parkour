import pygame
import sys
from settings import WIDTH, HEIGHT, BG_COLOR
from scripts.platforms import Platform
from player import Player
from level import Level

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = Player()
level = Level()

running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(level.platforms, dt)  # Pass dt to update
    level.update(dt)                    # Pass dt to update

    screen.fill(BG_COLOR)
    level.draw(screen)
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()