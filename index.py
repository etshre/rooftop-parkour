import pygame
import sys
import random
from scripts.entities import PhysicsEntity
from scripts.platforms import Platform

WIDTH, HEIGHT = 800, 600

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Scrolling Platformer")
        self.clock = pygame.time.Clock()

        self.movement = [False, False]  # [left, right]
        self.jumping = False
        self.jump_pressed_last = False  # To detect jump key press

        self.player = PhysicsEntity(self, 'player', (100, 518), (32, 32))

        # List of platforms (x, y, width, height)
        self.platforms = [
            Platform(0, 550, 800, 50),
            Platform(300, 450, 120, 20),
            Platform(600, 350, 120, 20),
            Platform(950, 500, 120, 20),
        ]

        self.scroll = 0  # How much the world has scrolled
        self.scroll_speed = 0
        self.failed = False

        self.score = 0
        self.best_score = 0

        self.last_platform = None  # Track last platform landed on

    def run(self):
        font = pygame.font.SysFont(None, 72)
        small_font = pygame.font.SysFont(None, 48)
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            self.screen.fill((14, 219, 248))

            # Always handle events
            mouse_clicked = False
            mouse_pos = (0, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if not self.failed:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = True
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = True
                        if event.key == pygame.K_UP:
                            self.jumping = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = False
                        if event.key == pygame.K_UP:
                            self.jumping = False
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_clicked = True
                        mouse_pos = event.pos

            if not self.failed:
                # Player movement: (right - left, vertical)
                move_x = (self.movement[1] - self.movement[0]) * 5

                # Jump as long as key is held and player is on ground
                self.player.update((move_x, 0), self.platforms, self.jumping, dt)

                # Smooth scrolling: move platforms left if player is at/after center and moving right
                if self.player.rect.centerx >= 400 and move_x > 0:
                    scroll_amount = move_x
                    self.player.pos[0] = 400 - self.player.size[0] // 2
                    self.scroll += scroll_amount
                    for platform in self.platforms:
                        platform.x -= scroll_amount

                # Score: +1 when landing on a new platform while moving right
                landed_platform = None
                for platform in self.platforms:
                    # Only check non-ground platforms
                    if platform.height < 50:
                        # Check if player is on top of platform
                        player_rect = self.player.rect
                        if (
                            abs(player_rect.bottom - platform.rect.top) < 5 and
                            player_rect.right > platform.rect.left + 5 and
                            player_rect.left < platform.rect.right - 5 and
                            self.player.velocity[1] == 0
                        ):
                            landed_platform = platform
                            break

                if (
                    landed_platform is not None and
                    landed_platform is not self.last_platform and
                    move_x > 0  # Only count if moving right
                ):
                    self.score += 1
                    self.last_platform = landed_platform

                # Recycle platforms that go off screen (faster spawn: smaller gap)
                for platform in self.platforms:
                    if platform.x + platform.width < 0 and platform.height < 50:
                        rightmost = max(
                            [p for p in self.platforms if p.height < 50 and p is not platform],
                            key=lambda p: p.x + p.width
                        )
                        max_step = 80
                        min_y = max(250, rightmost.y - max_step)
                        max_y = min(550, rightmost.y + max_step)
                        # Appear after rightmost or at right edge, whichever is further right
                        platform.x = max(WIDTH, rightmost.x + rightmost.width + random.randint(60, 120))
                        platform.y = random.randint(min_y, max_y)
                
                # Death check
                if self.player.pos[1] > HEIGHT:
                    self.failed = True
                    if self.score > self.best_score:
                        self.best_score = self.score

            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen)

            # Draw player or fail message
            if not self.failed:
                self.player.draw(self.screen)
            else:
                # Draw "You failed" message
                text = font.render("You failed womp womp", True, (255, 0, 0))
                rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
                self.screen.blit(text, rect)

                # Draw best score on fail screen
                best_score_text = small_font.render(f"Best: {self.best_score}", True, (0, 0, 0))
                best_score_rect = best_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
                self.screen.blit(best_score_text, best_score_rect)

                # Draw reset button
                button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 60)
                pygame.draw.rect(self.screen, (0, 200, 0), button_rect)
                pygame.draw.rect(self.screen, (0, 100, 0), button_rect, 4)
                button_text = small_font.render("Reset", True, (255, 255, 255))
                button_text_rect = button_text.get_rect(center=button_rect.center)
                self.screen.blit(button_text, button_text_rect)

                # Handle reset button click
                if mouse_clicked and button_rect.collidepoint(mouse_pos):
                    # Reset all game state
                    self.player = PhysicsEntity(self, 'player', (100, 518), (32, 32))
                    self.platforms = [
                        Platform(0, 550, 800, 50),
                        Platform(300, 450, 120, 20),
                        Platform(600, 350, 120, 20),
                        Platform(950, 500, 120, 20),
                    ]
                    self.scroll = 0
                    self.score = 0
                    self.failed = False
                    self.movement = [False, False]
                    self.jumping = False

            # Draw score (top right) and best score (top left)
            score_text = small_font.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
            best_score_text = small_font.render(f"Best: {self.best_score}", True, (0, 0, 0))
            self.screen.blit(best_score_text, (20, 20))

            pygame.display.update()

        pygame.quit()
        sys.exit()

Game().run()