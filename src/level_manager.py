import pygame
from settings import *
from support import *
from tile import Tile
from texture_manager import TextureManager
from ui import Box


class LevelManager:
    def __init__(self, obstacle_sprites):
        self.obstacle_sprites = obstacle_sprites
        self.display_surface = pygame.display.get_surface()

        # tiles
        self.texture_ids = {}
        self.tiles = []

        # sprite setup
        self.terrain_map = self.create_map()
        self.toches = [
            Box(pygame.Rect(0, 0, 10, 10), [])
        ]

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
                index = terrain_map[row][col]
                texture_id = self.texture_ids[index]
                surface = TextureManager.get_texture(texture_id)
                if self.is_solid(index):
                    tile = Tile((x, y), [self.obstacle_sprites], surface)
                else:
                    tile = Tile((x, y), [], surface)
                self.tiles.append(tile)

        return terrain_map

    def is_solid(self, tile_type):
        return tile_type != TILE.FLOOR.value and tile_type != TILE.FLOOR_ALT.value and tile_type != TILE.WALL_DOOR_UNLOCKED

    def add_tile(self, filepath, tile_type):
        texture_id = TextureManager.add_texture(filepath)
        self.texture_ids[tile_type] = texture_id

    def render_layer(self, renderer, layer):
        for row in range(self.rows):
            for col in range(self.cols):
                index = col + row * self.cols
                tile = self.tiles[index]
                renderer.render(tile)
