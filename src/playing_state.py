from texture_manager import TextureManager
from player import Player
from level_manager import LevelManager
from settings import *
from pygame import Vector2
from light_grid import LightGrid
from renderer import Renderer
from projectile import Projectile
from camera import Camera
import pygame
from pygame.sprite import Group


class PlayingState:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.obstacle_sprites = Group()
        self.entity_sprites = Group()
        self.light_grid_group = Group()
        self.player_projectiles = Group()
        self.camera = Camera()

        # move
        self.player = Player(
            (TILE_SIZE, TILE_SIZE),
            [self.entity_sprites],
            self.obstacle_sprites
        )

        self.level_manager = LevelManager(
            self.obstacle_sprites
        )
        self.light_grid = LightGrid(self.level_manager)

        self.renderer = Renderer(self.camera)

        self.project_texture_id = TextureManager.add_texture(
            "../resources/projectiles/spr_sword.png")

    def exit(self):
        pass

    def start(self):
        pass

    def update(self):
        self.player.update(self.camera)
        self.update_camera()
        self.update_attack()
        self.update_light()
        self.update_projectiles()

    def update_camera(self):
        self.camera.position = Vector2(self.player.rect.center)

    def update_attack(self):
        # todo - subtratct from mana
        if (self.player.is_attacking()):
            target = Vector2(self.player.aim_sprite.rect.center)
            Projectile(
                self.player.rect.center,
                [self.player_projectiles, self.entity_sprites],
                TextureManager.get_texture(self.project_texture_id),
                target
            )

    def update_light(self):
        self.light_grid.update(self.player)

    def update_projectiles(self):
        for projectile in self.player_projectiles:
            projectile.update()

    def render(self):
        for layer in range(self.level_manager.layers):
            self.level_manager.render_layer(self.renderer, layer)
            for sprite in self.entity_sprites.sprites():
                self.renderer.add_to_render_batch(sprite)
            self.renderer.render_batch()
        self.light_grid.render(self.renderer)
        self.renderer.render(self.player.aim_sprite)
