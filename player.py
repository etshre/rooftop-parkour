import pygame
from game_settings import *

class Player:
    def __init__(self):
        self.image = pygame.Surface((40, 60))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 150

        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_RIGHT]:
            self.rect.x += 200 * 1/60

        # Gravity
        self.vel_y += GRAVITY * 1/60
        self.rect.y += self.vel_y * 1/60

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_VELOCITY

        # Collision check
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
