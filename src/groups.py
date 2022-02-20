from operator import imod


import pygame
from player import Player


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # render sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if (player == sprite):
                continue
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        offset_pos = player.rect.topleft - self.offset
        self.display_surface.blit(player.image, offset_pos)


class BoundingBoxDebugGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # render sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            bbox = pygame.Rect(sprite.hitbox)
            bbox.topleft = (sprite.hitbox.topleft - self.offset)
            if isinstance(sprite, Player):
                pygame.draw.rect(self.display_surface, (0, 255, 0), bbox, 2)
            else:
                pygame.draw.rect(self.display_surface, (0, 255, 255), bbox, 2)


class BoundingBoxUIDebugGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self):
        # render sprites
        for sprite in self.sprites():
            pygame.draw.rect(self.display_surface, (0, 255, 0), sprite.rect, 1)
