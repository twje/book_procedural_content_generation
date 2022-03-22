from ctypes.wintypes import POINT
from enum import Enum
from enum import auto
from msilib.schema import Class

# game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60


# tiles
TILE_SIZE = 50

# MAX SPAWNS
MAX_ITEM_SPAWN_COUNT = 50
MAX_ENEMY_SPAWN_COUNT = 20


class TILE(Enum):
    WALL_SINGLE = 0
    WALL_TOP_END = auto()
    WALL_SIDE_RIGHT_END = auto()
    WALL_BOTTOM_LEFT = auto()
    WALL_BOTTOM_END = auto()
    WALL_SIDE = auto()
    WALL_TOP_LEFT = auto()
    WALL_SIDE_LEFT_T = auto()
    WALL_SIDE_LEFT_END = auto()
    WALL_BOTTOM_RIGHT = auto()
    WALL_TOP = auto()
    WALL_BOTTOM_T = auto()
    WALL_TOP_RIGHT = auto()
    WALL_SIDE_RIGHT_T = auto()
    WALL_TOP_T = auto()
    WALL_INTERSECTION = auto()
    WALL_DOOR_LOCKED = auto()
    WALL_DOOR_UNLOCKED = auto()
    WALL_ENTRANCE = auto()
    FLOOR = auto()
    FLOOR_ALT = auto()
    EMPTY = auto()


class ANIMATION_STATE(Enum):
    WALK_UP = 0
    WALK_DOWN = auto()
    WALK_RIGHT = auto()
    WALK_LEFT = auto()
    IDLE_UP = auto()
    IDLE_DOWN = auto()
    IDLE_RIGHT = auto()
    IDLE_LEFT = auto()


class GAME_STATE(Enum):
    PLAYING = 0


class ITEM_TYPE(Enum):
    GOLD = 0
    GEM = auto()
    KEY = auto()
    POTION = auto()
    HEART = auto()


class STAT_TYPE(Enum):
    ATTACK = 0
    DEFENCE = auto()
    STRENGTH = auto()
    DEXTERITY = auto()
    SETMINA = auto()
