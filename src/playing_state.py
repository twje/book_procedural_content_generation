import random
from traceback import print_tb
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
from slime import Slime
from humanoid import Humanoid


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
        self.spawn_items()
        self.spawn_enemies()

    def spawn_items(self):
        for _ in range(MAX_ITEM_SPAWN_COUNT):
            if random.randint(0, 1):
                item_type = random.choice([Gold, Gem])
                self.spawn_item(item_type)

    def spawn_item(self, item_type, position=None):
        if position is None:
            spawn_location = self.level_manager.get_random_spawn_location()
        else:
            spawn_location = position
        item_type(spawn_location, [self.items])

    def spawn_enemies(self):
        for _ in range(MAX_ENEMY_SPAWN_COUNT):
            if random.randint(0, 1):
                enemy_type = random.choice([Slime, Humanoid])
                self.spawn_enemy(enemy_type)

    def spawn_enemy(self, enemy_type, position=None):
        if position is None:
            spawn_location = self.level_manager.get_random_spawn_location()
        else:
            spawn_location = position
        enemy_type(spawn_location, [self.enemies])

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
                self.game.reset_ui()

    def update_light(self):
        self.light_grid.update(self.player)

    def update_items(self):
        refresh_ui = False
        for item in self.items:
            item.update()
            if not self.player_collised_with_item(item):
                continue

            if item.typez == ITEM_TYPE.GOLD:
                self.game.add_gold(item.value)
                refresh_ui = True
            elif item.typez == ITEM_TYPE.GEM:
                self.game.add_gem(item.value)
                refresh_ui = True
            elif item.typez == ITEM_TYPE.KEY:
                pass
            elif item.typez == ITEM_TYPE.POTION:
                pass
            elif item.typez == ITEM_TYPE.HEART:
                pass
            item.kill()

        if refresh_ui:
            self.game.reset_ui()

    def player_collised_with_item(self, item):
        player_pos = Vector2(self.player.rect.center)
        distance = player_pos.distance_to(item.rect.center)
        return distance < 40

    def update_enemies(self):
        for enemy in self.enemies:
            for projectile in self.projectiles:
                if not enemy.rect.colliderect(projectile):
                    continue
                enemy.take_demage(25)
                if enemy.is_dead():
                    position = enemy.rect.center

                projectile.kill()

    def update_projectiles(self):  # implement
        for projectile in self.projectiles:
            for obstacle in self.obstacle_sprites:
                if obstacle.rect.colliderect(projectile.rect):
                    projectile.kill()
                else:
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
