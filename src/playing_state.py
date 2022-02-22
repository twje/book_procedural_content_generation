from tile import Tile
from ui import SpriteElement
from texture_manager import TextureManager
from player import Player
from level_manager import LevelManager
from settings import *
from pygame import Vector2
import groups
import pygame
from groups import get_relative_position


class PlayingState:
    def __init__(self, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = groups.YSortCameraGroup()
        self.light_grid_sprites = groups.YSortCameraGroup()
        self.torches_group = groups.YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player(
            (TILE_SIZE, TILE_SIZE),
            [self.visible_sprites],
            self.obstacle_sprites
        )
        self.level_manager = LevelManager(
            self.visible_sprites,
            self.obstacle_sprites
        )

        self.construct_light_grid()

    def construct_light_grid(self):
        texture_id = TextureManager.add_texture(
            "../resources/spr_light_grid.png")
        texture = TextureManager.get_texture(texture_id)

        cols = self.level_manager.width // texture.get_width()
        rows = self.level_manager.height // texture.get_height()
        for row in range(rows):
            for col in range(cols):
                x = row * texture.get_width()
                y = col * texture.get_height()
                sprite = SpriteElement(
                    (x, y), [self.light_grid_sprites], texture)
                # self.light_grid.append(sprite)

        for torch in self.level_manager.toches:
            self.torches_group.add(torch)

    def exit(self):
        pass

    def start(self):
        pass

    def update(self):
        self.player.update()
        self.update_light()

        for sprite in self.light_grid_sprites:
            tile_alpha = 255

            sprite_pos = get_relative_position(self.player, sprite)
            distance = sprite_pos.distance_to(self.player.rect.center)
            if distance < 200:
                tile_alpha = 0
            # elif distance < 250:
            #     tile_alpha = (51 - (distance - 200)) / 10

            # for torch in self.level_manager.toches:
            #     sprite_pos = Vector2(sprite.rect.center)
            #     distance = sprite_pos.distance_to(torch.rect.center)
            #     if distance < 100:
            #         tile_alpha -= (tile_alpha -
            #                        ((tile_alpha/100) * distance)) * 0.5
            # if tile_alpha < 0:
            #     tile_alpha = 0

            sprite.image.set_alpha(tile_alpha)

    def update_light(self):
        pass

    def render(self):
        self.visible_sprites.custom_draw(self.player)
        # self.light_grid_sprites.custom_draw(self.player)
        self.torches_group.custom_draw(self.player)
