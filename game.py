import pygame
import sys
from scripts.entities import PhysicsEntity

class Game:
    def __init__(self): #initaliseing the game

        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Platformer Game")

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

    def run(self): #how the game runs

        while True:
            self.screen.fill((14, 219, 248))

            self.player.update((self.movement[1] - self.movement[0], 0))
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60) #running at 60 fps

Game().run()