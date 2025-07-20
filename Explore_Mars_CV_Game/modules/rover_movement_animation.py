import random
import pygame
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 30
        self.color = (139, 69, 19)  # Martian dust color
        self.size = random.randint(3, 6)
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-1, 2)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = max(0, int(255 * (self.life / 30)))
            dust_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(dust_surface, (*self.color, alpha), (self.size // 2, self.size // 2), self.size // 2)
            surface.blit(dust_surface, (self.x, self.y))