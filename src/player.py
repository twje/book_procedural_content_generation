import random
import pygame
from settings import *
from animation import Animation
from texture_manager import TextureManager
from ui import SpriteElement
from entity import Entity


class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.debug = True
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
        self.attacking = False
        self.attack_delta = pygame.time.get_ticks()

        # aim sprite
        texture_id = TextureManager.add_texture("../resources/ui/spr_aim.png")
        self.aim_sprite = SpriteElement(
            (0, 0),
            [],
            TextureManager.get_texture(texture_id)
        )
        self.aim_sprite.debug = True

        # HP/MP
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50

        # STATS
        self.stat_points = 50
        bias = [random.random() for _ in range(5)]
        total = sum(bias)
        self.attack = round(self.stat_points * (bias[0] / total))
        self.defence = round(self.stat_points * (bias[1] / total))
        self.strength = round(self.stat_points * (bias[2] / total))
        self.dexterity = round(self.stat_points * (bias[3] / total))
        self.stemina = round(self.stat_points * (bias[4] / total))

    # properties

    def add_health(self, value):
        self.health = max(0, self.health + value)

    def add_mana(self, value):
        self.mana = max(0, self.mana + value)

    @property
    def health_percentage(self):
        return self.health/self.max_health

    @property
    def mana_percentage(self):
        return self.mana/self.max_mana

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

        # attack input
        elapsed_attack_time = pygame.time.get_ticks() - self.attack_delta
        if elapsed_attack_time > 255:
            if keys[pygame.K_SPACE]:
                self.attacking = True

    def is_attacking(self):
        if self.attacking:
            self.attacking = False
            self.attack_delta = pygame.time.get_ticks()
            return True
        else:
            return False

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

    def aim(self, camera):
        x, y = pygame.mouse.get_pos()
        position = camera.world_coordinates((x, y))
        self.aim_sprite.rect.center = pygame.Vector2(position)

    def update(self, camera):
        self.input()
        self.get_status()
        self.animate()
        self.aim(camera)
        self.move(self.speed)
