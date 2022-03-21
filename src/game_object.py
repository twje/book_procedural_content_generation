import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug = False
        self.z = 0    