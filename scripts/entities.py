import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0.0, 0.0]
        self.on_ground = False

    @property
    def rect(self):
        return pygame.Rect(int(self.pos[0]), int(self.pos[1]), self.size[0], self.size[1])

    def update(self, movement=(0,0), platforms=None, jumping=False, dt=1/60):
        if platforms is None:
            platforms = []

        GRAVITY = 30  # pixels/sec^2 normally 30
        JUMP_VELOCITY = -11  # pixels/sec (higher jump) normally 13
        ACCEL = 60  # horizontal acceleration (pixels/sec^2) normally 60
        MAX_SPEED = 7  # max horizontal speed normally 7
        FRICTION = 40  # friction (pixels/sec^2) normally 40

        # Horizontal movement with acceleration and friction
        if movement[0] > 0:
            self.velocity[0] += ACCEL * dt
        elif movement[0] < 0:
            self.velocity[0] -= ACCEL * dt
        else:
            # Apply friction
            if self.velocity[0] > 0:
                self.velocity[0] -= FRICTION * dt
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            elif self.velocity[0] < 0:
                self.velocity[0] += FRICTION * dt
                if self.velocity[0] > 0:
                    self.velocity[0] = 0

        # Clamp horizontal speed
        if self.velocity[0] > MAX_SPEED:
            self.velocity[0] = MAX_SPEED
        if self.velocity[0] < -MAX_SPEED:
            self.velocity[0] = -MAX_SPEED

        # Jumping (only trigger jump if just pressed and on ground)
        if jumping and self.on_ground:
            self.velocity[1] = JUMP_VELOCITY

        # Gravity
        self.velocity[1] += GRAVITY * dt
        if self.velocity[1] > 15:
            self.velocity[1] = 15

        # Move horizontally and check for collisions
        self.pos[0] += self.velocity[0]
        entity_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        for platform in platforms:
            if entity_rect.colliderect(platform.rect):
                if self.velocity[0] > 0:
                    self.pos[0] = platform.rect.left - self.size[0]
                    self.velocity[0] = 0
                elif self.velocity[0] < 0:
                    self.pos[0] = platform.rect.right
                    self.velocity[0] = 0

        # Move vertically and check for collisions
        self.pos[1] += self.velocity[1]
        entity_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.on_ground = False
        for platform in platforms:
            if entity_rect.colliderect(platform.rect):
                if self.velocity[1] > 0:
                    self.pos[1] = platform.rect.top - self.size[1]
                    self.velocity[1] = 0
                    self.on_ground = True
                elif self.velocity[1] < 0:
                    self.pos[1] = platform.rect.bottom
                    self.velocity[1] = 0

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), (int(self.pos[0]), int(self.pos[1]), self.size[0], self.size[1]))