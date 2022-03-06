import pygame
from pygame import Vector2


class Camera:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.position = Vector2()

    # def render_player(self):
    #     offset_pos = self.screen_position(self.player.rect.topleft)
    #     self.display_surface.blit(self.player.image, offset_pos)

    def screen_position(self, world_coords):
        # self.offset.x = self.player.rect.centerx - self.half_width
        # self.offset.y = self.player.rect.centery - self.half_height

        self.offset.x = self.position.x - self.half_width
        self.offset.y = self.position.y - self.half_height
        return Vector2(world_coords) - self.offset

    def world_coordinates(self, screen_coords):
        # self.offset.x = self.player.rect.centerx - self.half_width
        # self.offset.y = self.player.rect.centery - self.half_height

        self.offset.x = self.position.x - self.half_width
        self.offset.y = self.position.y - self.half_height
        return Vector2(screen_coords) + self.offset
