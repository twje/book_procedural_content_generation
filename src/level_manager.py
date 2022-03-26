import random
import pygame
from settings import *
from support import *
from tile import Tile
from torch import Torch
from texture_manager import TextureManager
from pygame import Vector2


class LevelManager:
    def __init__(self, obstacle_sprites):
        self.obstacle_sprites = obstacle_sprites
        self.display_surface = pygame.display.get_surface()

        # tiles
        self.texture_ids = {}
        self.tiles = []

        # sprite setup
        self.torches = pygame.sprite.Group()
        self.terrain_map = self.create_map()

    def create_map(self):
        self.add_tile(
            "../resources/tiles/spr_tile_floor.png",
            TILE.FLOOR.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_top.png",
            TILE.WALL_TOP.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_top_left.png",
            TILE.WALL_TOP_LEFT.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_top_right.png",
            TILE.WALL_TOP_RIGHT.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_top_t.png",
            TILE.WALL_TOP_T.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_top_end.png",
            TILE.WALL_TOP_END.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_bottom_left.png",
            TILE.WALL_BOTTOM_LEFT.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_bottom_right.png",
            TILE.WALL_BOTTOM_RIGHT.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_bottom_t.png",
            TILE.WALL_BOTTOM_T.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_bottom_end.png",
            TILE.WALL_BOTTOM_END.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_side.png",
            TILE.WALL_SIDE.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_side_left_t.png",
            TILE.WALL_SIDE_LEFT_T.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_side_left_end.png",
            TILE.WALL_SIDE_LEFT_END.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_side_right_t.png",
            TILE.WALL_SIDE_RIGHT_T.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_side_right_end.png",
            TILE.WALL_SIDE_RIGHT_END.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_intersection.png",
            TILE.WALL_INTERSECTION.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_single.png",
            TILE.WALL_SINGLE.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_wall_entrance.png",
            TILE.WALL_ENTRANCE.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_door_locked.png",
            TILE.WALL_DOOR_LOCKED.value
        )
        self.add_tile(
            "../resources/tiles/spr_tile_door_unlocked.png",
            TILE.WALL_DOOR_UNLOCKED.value
        )

        # map state
        terrain_map = import_map_layout('../resources/data/level_data.txt')
        self.rows = len(terrain_map)
        self.cols = len(terrain_map[0])
        self.tile_size = TILE_SIZE
        self.width = self.cols * self.tile_size
        self.height = self.rows * self.tile_size
        self.layers = 1

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.tile_size
                y = row * self.tile_size
                tile_type = terrain_map[row][col]
                texture_id = self.texture_ids[tile_type]
                surface = TextureManager.get_texture(texture_id)
                if self.is_solid(tile_type):
                    groups = [self.obstacle_sprites]
                else:
                    groups = []
                self.tiles.append(
                    Tile(
                        tile_type,
                        Vector2(col, row),
                        Vector2(x, y),
                        groups,
                        surface
                    )
                )

        # torches
        for torch_pos in (
            Vector2(3, 9),
            Vector2(7, 7),
            Vector2(11, 11),
            Vector2(13, 15),
            Vector2(15, 3),
        ):
            pos_x = torch_pos.x * self.tile_size + self.tile_size/2
            pos_y = torch_pos.y * self.tile_size + self.tile_size/2
            Torch((pos_x, pos_y), self.torches)

        return terrain_map

    def is_solid(self, tile_type):
        return tile_type != TILE.FLOOR.value and tile_type != TILE.FLOOR_ALT.value and tile_type != TILE.WALL_DOOR_UNLOCKED

    def is_floor(self, tile_x, tile_y):
        index = tile_x + tile_y * self.cols
        tile_type = self.tiles[int(index)].tile_type
        return tile_type == TILE.FLOOR.value or tile_type == TILE.FLOOR_ALT.value

    def get_random_spawn_location(self):
        col_index = 0
        row_index = 0
        while not self.is_floor(col_index, row_index):
            col_index = random.randint(0, self.cols - 1)
            row_index = random.randint(0, self.rows - 1)

        tile_location = self.get_actual_tile_location(col_index, row_index)
        tile_location.x += random.randint(-10, 10)
        tile_location.y += random.randint(-10, 10)

        return tile_location

    def get_actual_tile_location(self, tile_x, tile_y):
        pos_x = tile_x * self.tile_size + self.tile_size/2
        pos_y = tile_y * self.tile_size + self.tile_size/2
        return Vector2(pos_x, pos_y)

    def add_tile(self, filepath, tile_type):
        texture_id = TextureManager.add_texture(filepath)
        self.texture_ids[tile_type] = texture_id

    def get_tile(self, position):
        tile_x = round(position[0]/self.tile_size)
        tile_y = round(position[1]/self.tile_size)
        index = tile_x + tile_y * self.cols
        return self.tiles[index]

    def render_layer(self, renderer, layer):
        for row in range(self.rows):
            for col in range(self.cols):
                index = col + row * self.cols
                tile = self.tiles[index]
                renderer.render(tile)
