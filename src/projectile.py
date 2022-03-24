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
    def __init__(self, position, groups, obstacle_sprites, surface, target):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites
        self.position = Vector2(position)
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
        self.position.x += self.velocity.x * delta * 500
        self.collision('horizontal')
        self.position.y += self.velocity.y * delta * 500
        self.collision('vertical')
        self.rotate(delta)
        self.rect.center = (round(self.position.x), round(self.position.y))

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.rect):
                    self.kill()

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.rect):
                    self.kill()

    def rotate(self, delta):
        self.angle += 400 * delta
        self.rotate_transform.angle = self.angle
        self.transform.update()
