from cmath import rect
import pygame
from game_object import GameObject


class SpriteElement(GameObject):
    def __init__(self, position, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)


class Bar(GameObject):
    def __init__(self, position, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.image_copy = surface
        self.rect = self.image.get_rect(topleft=position)

    def set_width(self, percent):
        width = self.rect.width * percent
        self.image = pygame.transform.scale(
            self.image_copy,
            (width, self.rect.height)
        )


class TextElement(GameObject):
    def __init__(self, position, groups, text, min_width=-1, min_height=-1, centerx=False, centery=False):
        super().__init__(groups)
        font = pygame.font.Font(None, 30)
        self.text = font.render(text, True, 'White')
        self.rect = self.text.get_rect(topleft=position)

        if min_width >= 0:
            self.rect.width = max(self.rect.width, min_width)
        if min_height >= 0:
            self.rect.height = max(self.rect.height, min_height)

        bbox = self.text.get_rect(topleft=position)
        offset = pygame.Vector2(self.rect.topleft)
        if centerx:
            offset.x = self.rect.centerx - bbox.width/2
        if centery:
            offset.y = self.rect.centery - bbox.height/2

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.image.blit(self.text, (offset.x, offset.y))


class Box(GameObject):
    def __init__(self, rect, groups):
        super().__init__(groups)
        self.rect = rect
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (0, 255, 255), self.rect, 1)
