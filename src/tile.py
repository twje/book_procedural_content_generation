import pygame
from settings import *
from game_object import GameObject


class Tile(GameObject):
    def __init__(self, tile_type, index, position, groups, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.tile_type = tile_type
        self.index = index
        self.position = position
        self.image = surface
        self.rect = self.image.get_rect(topleft=self.position)
        self.hitbox = self.rect.inflate(0, 0)
