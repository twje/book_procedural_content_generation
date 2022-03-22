import pygame
from pygame import Vector2
from game_object import GameObject


class RotateTransform:
    def __init__(self, angle=0):
        self.angle = angle

    def update(self, image):
        rotated_image = pygame.transform.rotate(image, self.angle)
        return rotated_image


class Transform:
    def __init__(self, surface):
        self.image = surface
        self.transformed_image = self.image
        self.transforms = []

    def add_transform(self, transform):
        self.transforms.append(transform)

    def update(self):
        if len(self.transforms) == 0:
            return self.image

        self.transformed_image = self.image
        for transform in reversed(self.transforms):
            self.transformed_image = transform.update(self.transformed_image)
        return self.transformed_image


class Projectile(GameObject):
    def __init__(self, position, groups, surface, target):
        super().__init__(groups)
        self.position = position
        self.transform = Transform(surface)
        self.rotate_transform = RotateTransform(45)
        self.rect = self.image.get_rect(center=position)
        self.timestamp = pygame.time.get_ticks()
        self.velocity = (target - self.rect.center).normalize()
        self.debug = True
        self.angle = 0

        self.transform.add_transform(self.rotate_transform)

    @property
    def image(self):
        return self.transform.transformed_image

    def update(self):
        delta = (pygame.time.get_ticks() - self.timestamp)/1000
        self.timestamp = pygame.time.get_ticks()
        self.position += self.velocity * delta * 500
        self.rotate(delta)
        self.rect.center = (round(self.position.x), round(self.position.y))

    def rotate(self, delta):
        self.angle += 400 * delta
        self.rotate_transform.angle = self.angle
        self.transform.update()
