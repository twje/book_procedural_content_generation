import pygame
from pygame import Vector2


class Renderer:
    def __init__(self, camera):
        self.camera = camera
        self.display_surface = pygame.display.get_surface()
        self.sprites = []

    def render(self, sprite):
        offset_pos = self.camera.screen_position(sprite.rect.topleft)
        self.display_surface.blit(sprite.image, offset_pos)
        if sprite.debug:
            try:
                rect = sprite.hitbox.copy()
            except:
                rect = sprite.rect.copy()
            rect.topleft = offset_pos
            pygame.draw.rect(
                self.display_surface,
                (0, 255, 0),
                rect,
                1
            )

    def render_batch(self):
        for sprite in sorted(self.sprites, key=lambda sprite: sprite.rect.centery):
            self.render(sprite)
        self.sprites.clear()

    def add_to_render_batch(self, *sprites):
        for sprite in sprites:
            self.sprites.append(sprite)
