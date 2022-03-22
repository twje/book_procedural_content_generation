import random
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
from gold import Gold
from gem import Gem


class PlayingState:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.obstacle_sprites = Group()
        self.projectiles = Group()
        self.items = Group()
        self.enemies = Group()
        self.light_grid_group = Group()
        self.player_projectiles = Group()
        self.camera = Camera()

        # move
        self.player = Player(
            (TILE_SIZE, TILE_SIZE),
            [],
            self.obstacle_sprites
        )

        self.level_manager = LevelManager(
            self.obstacle_sprites
        )
        self.light_grid = LightGrid(self.level_manager)

        self.renderer = Renderer(self.camera)

        self.project_texture_id = TextureManager.add_texture(
            "../resources/projectiles/spr_sword.png")

        self.populate_level()

    def exit(self):
        pass

    def start(self):
        pass

    def populate_level(self):
        if random.randint(0, 1):
            Gold((300, 100), [self.items])

        if random.randint(0, 1):
            Gem((200, 200), [self.items])

    # --------------
    # update methods
    # --------------
    def update(self):
        self.player.update(self.camera)
        self.update_camera()
        self.update_attack()
        self.update_light()
        self.update_items()
        self.update_enemies()
        self.update_projectiles()

    def update_camera(self):
        self.camera.position = Vector2(self.player.rect.center)

    def update_attack(self):
        if (self.player.is_attacking()):
            mana_required = 2
            if self.player.mana >= mana_required:
                target = Vector2(self.player.aim_sprite.rect.center)
                Projectile(
                    self.player.rect.center,
                    [self.projectiles],
                    TextureManager.get_texture(self.project_texture_id),
                    target
                )
                self.player.add_mana(-mana_required)
                self.game.update_mana_bar(self.player.mana_percentage)

    def update_light(self):
        self.light_grid.update(self.player)

    def update_items(self):
        for item in self.items:
            item.update()
            if not self.player_collised_with_item(item):
                continue

            if item.typez == ITEM_TYPE.GOLD:
                self.game.add_gold(item.value)
            elif item.typez == ITEM_TYPE.GEM:
                self.game.add_gem(item.value)
            elif item.typez == ITEM_TYPE.KEY:
                pass
            elif item.typez == ITEM_TYPE.POTION:
                pass
            elif item.typez == ITEM_TYPE.HEART:
                pass
            item.kill()

    def player_collised_with_item(self, item):
        player_pos = Vector2(self.player.rect.center)
        distance = player_pos.distance_to(item.rect.center)
        return distance < 40

    def update_enemies(self):
        pass

    def update_projectiles(self):  # implement
        for projectile in self.projectiles:
            projectile.update()

    # --------------
    # render methods
    # --------------
    def render(self):
        for layer in range(self.level_manager.layers):
            self.render_level(layer)
            self.render_player(layer)
            self.render_entities(layer)
            self.render_items(layer)
            self.render_enemies(layer)
            self.renderer.render_batch()
        self.light_grid.render(self.renderer)
        self.renderer.render(self.player.aim_sprite)
        self.render_stats()

    def render_level(self, layer):
        self.level_manager.render_layer(self.renderer, layer)

    def render_player(self, layer):
        if layer == self.player.z:
            self.renderer.add_to_render_batch(self.player)

    def render_entities(self, layer):
        for sprite in self.projectiles.sprites():
            if sprite.z == layer:
                self.renderer.add_to_render_batch(sprite)

    def render_items(self, layer):
        for sprite in self.items:
            if sprite.z == layer:
                self.renderer.add_to_render_batch(sprite)

    def render_enemies(self, layer):
        for sprite in self.enemies:
            if sprite.z == layer:
                self.renderer.add_to_render_batch(sprite)

    def render_stats(self):
        is_stat_different = False
        for stat_type, value in self.player.stats.items():
            if self.game.get_stat(stat_type) != value:
                self.game.set_stat(stat_type, value)
                is_stat_different = True

        # be efficient
        if is_stat_different:
            self.game.reset_ui()
