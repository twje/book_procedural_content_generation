import pygame
from settings import *
from game_object import GameObject


class Tile(GameObject):
    def __init__(self, position, groups, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, 0)
