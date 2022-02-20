from msilib import sequence
import pygame
from settings import *
from animation import Animation
from texture_manager import TextureManager


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 4

        # load textures
        self.texture_ids = {}
        anim_states = [
            (ANIMATION_STATE.WALK_UP.value,
             "../resources/players/warrior/spr_warrior_walk_up.png"),
            (ANIMATION_STATE.WALK_RIGHT.value,
             "../resources/players/warrior/spr_warrior_walk_right.png"),
            (ANIMATION_STATE.WALK_DOWN.value,
             "../resources/players/warrior/spr_warrior_walk_down.png"),
            (ANIMATION_STATE.WALK_LEFT.value,
             "../resources/players/warrior/spr_warrior_walk_left.png"),
            (ANIMATION_STATE.IDLE_UP.value,
             "../resources/players/warrior/spr_warrior_idle_up.png"),
            (ANIMATION_STATE.IDLE_RIGHT.value,
             "../resources/players/warrior/spr_warrior_idle_right.png"),
            (ANIMATION_STATE.IDLE_DOWN.value,
             "../resources/players/warrior/spr_warrior_idle_down.png"),
            (ANIMATION_STATE.IDLE_LEFT.value,
             "../resources/players/warrior/spr_warrior_idle_left.png")
        ]
        for anim_state in anim_states:
            self.texture_ids[anim_state[0]
                             ] = TextureManager.add_texture(anim_state[1])

        # init animation
        self.animation = Animation()

        for anim_state in anim_states[:4]:
            self.animation.add_sequence(
                anim_state[0],
                self.texture_ids[anim_state[0]],
                8,
                0.15
            )
        for anim_state in anim_states[-4:]:
            self.animation.add_sequence(
                anim_state[0],
                self.texture_ids[anim_state[0]],
                1,
                0
            )

        self.animation_sequence = ANIMATION_STATE.IDLE_UP.value

        # init sprite
        self.animation.set_sequence(self.animation_sequence)
        self.image = self.animation.get_frame()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, 0)

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.animation_sequence = ANIMATION_STATE.WALK_UP.value
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.animation_sequence = ANIMATION_STATE.WALK_DOWN.value
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.animation_sequence = ANIMATION_STATE.WALK_RIGHT.value
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.animation_sequence = ANIMATION_STATE.WALK_LEFT.value
        else:
            self.direction.x = 0

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if self.animation_sequence < 4:
                self.animation_sequence += 4

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        self.animation.set_sequence(self.animation_sequence)
        self.animation.update()
        self.image = self.animation.get_frame()

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
