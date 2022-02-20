from select import select
import pygame


def import_map_layout(path):
    terrain_map = []
    with open(path) as level_map:
        for line in level_map.readlines():
            data = [int(tile_id) for tile_id in line.replace("][", ",")
                    .replace("[", "")
                    .replace("]", "")
                    .strip()
                    .split(",")]
            terrain_map.append(data)

    return terrain_map
