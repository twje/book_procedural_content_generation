import pygame
from game_object import GameObject


class Projectile(GameObject):
    def __init__(self, position, groups, surface, target):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.target = target
        self.timestamp = pygame.time.get_ticks()
        self.velocity = (target - position).normalize()

    def update(self):
        delta = (pygame.time.get_ticks() - self.timestamp)/1000
        self.timestamp = pygame.time.get_ticks()
        self.rect.move_ip(self.velocity * delta * 500)
