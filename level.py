import random
from platforms import Platform
from game_settings import *

class Level:
    def __init__(self):
        self.platforms = [Platform(100, 500), Platform(300, 400), Platform(550, 450)]
        self.timer = 0
        self.spawn_delay = 2  # seconds
        self.scroll_speed = 200  # pixels/sec

    def update(self):
        for platform in self.platforms:
            platform.update(self.scroll_speed * 1/60)

        # Remove platforms that are off-screen
        self.platforms = [p for p in self.platforms if p.rect.right > 0]

        # Spawn new platforms
        self.timer += 1/60
        if self.timer >= self.spawn_delay:
            self.timer = 0
            last_y = self.platforms[-1].rect.y
            new_y = max(200, min(HEIGHT - 100, last_y + random.randint(-100, 100)))
            new_x = self.platforms[-1].rect.x + random.randint(250, 350)
            self.platforms.append(Platform(new_x, new_y))

    def draw(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
