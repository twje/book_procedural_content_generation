from collections import abc
from collections import defaultdict
import math
import pygame


# --------------
# Helper Methods
# --------------
def bounding_box(sprite_group):
    """Compute sprite group bounding box."""
    rect = pygame.Rect(sprite_group[0].rect)
    for sprite in sprite_group:
        rect = sprite.rect.union(rect)
    return rect


def global_bounding_box(sprite_groups):
    """Compute combined bounding box of all sprite groups."""
    rect = bounding_box(sprite_groups[0])
    for sprite_group in sprite_groups:
        rect = bounding_box(sprite_group).union(rect)
    return rect


def convert_to_sprite_groups(values):
    """Convert every element in list to a sprite group."""
    result = []
    for value in values:
        if isinstance(value, list):
            result.append(value)
        else:
            result.append([value])
    return result


def normalize_weights(weights):
    """Return default dict of normalized weights"""
    if weights is not None:
        if isinstance(weights, int):
            result = defaultdict(lambda: weights)
        elif isinstance(weights, abc.Mapping):
            result = defaultdict(lambda: 0)
            for key, value in weights.items():
                result[key] = value
    else:
        result = defaultdict(lambda: 0)

    return result


def compute_max_col_widths(sprite_groups, cols, rows):
    """Return dict of max width indexed by column"""
    max_col_widths = defaultdict(lambda: 0)
    for row in range(rows):
        for col in range(cols):
            index = col + row * cols
            if index >= len(sprite_groups):
                continue
            sprite_group = sprite_groups[index]
            width = bounding_box(sprite_group).width
            max_col_widths[col] = max(max_col_widths[col], width)

    return max_col_widths


def compute_max_col_width(sprite_groups):
    """Return max sprite_group width"""
    max_col_widths = compute_max_col_widths(
        sprite_groups,
        len(sprite_groups),
        1
    )
    return max(max_col_widths.values())


def screen_rect():
    display_surface = pygame.display.get_surface()
    return display_surface.get_rect()


# -----------------
# Layout Algorithms
# -----------------
def move(x, y, *sprites):
    """"""
    sprite_groups = convert_to_sprite_groups(sprites)
    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.left += x
            sprite.rect.top += y


def justify_left(sprites, target):
    """Align left of sprites global bounding box with left of target."""
    sprite_groups = convert_to_sprite_groups(sprites)
    bbox = global_bounding_box(sprite_groups)
    offset = target.left - bbox.left
    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.left += offset


def justify_top(sprites, target):
    """Align top of sprites global bounding box with top of target."""
    sprite_groups = convert_to_sprite_groups(sprites)
    bbox = global_bounding_box(sprite_groups)
    offset = target.top - bbox.top
    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.top += offset


def justify_right(sprites, target):
    """Align right of sprites global bounding box with right of target."""
    pass


def justify_bottom(sprites, target):
    """Align bottom of sprites global bounding box with bottom of target."""
    pass


def position_sprite_group_left(sprite_group, value):
    """Left justify sprite group by value."""
    bbox = bounding_box(sprite_group)
    for sprite in sprite_group:
        offsetx = sprite.rect.left - bbox.left
        sprite.rect.left = value + offsetx
    return bbox.width


def position_sprite_group_top(sprite_group, value):
    """"""
    pass


def stack_hort(sprites, cols=None, weights=None):
    """Left justify sprites seperated by weights."""
    sprite_groups = convert_to_sprite_groups(sprites)
    cols = len(sprite_groups) if cols is None else cols
    rows = math.ceil(len(sprite_groups)/cols)
    weights = normalize_weights(weights)
    max_col_widths = compute_max_col_widths(sprite_groups, cols, rows)

    # layout
    left = global_bounding_box(sprite_groups).left
    for row in range(rows):
        offset = 0
        for col in range(cols):
            index = col + row * cols
            if index >= len(sprite_groups):
                continue
            sprite_group = sprite_groups[index]
            offset += weights[col]
            position_sprite_group_left(sprite_group, left + offset)
            offset += max_col_widths[col]


def distribute_hort(sprites, cols=None, span=0):
    """Evenly distribute sprites horizontally relative to their global bounding box."""
    sprite_groups = convert_to_sprite_groups(sprites)
    cols = len(sprite_groups) if cols is None else cols
    rows = math.ceil(len(sprite_groups)/cols)
    max_col_width = max(compute_max_col_width(sprite_groups), span)

    # layout
    weights = defaultdict(lambda: [0, 0])
    for row in range(rows):
        for col in range(cols):
            index = col + row * cols
            if index >= len(sprite_groups):
                continue
            sprite_group = sprite_groups[index]
            space = max_col_width - bounding_box(sprite_group).width
            weights[index][0] = space/2
            weights[index][1] = space/2

    left = global_bounding_box(sprite_groups).left
    for row in range(rows):
        offset = 0
        for col in range(cols):
            index = col + row * cols
            if index >= len(sprite_groups):
                continue
            sprite_group = sprite_groups[index]
            position_sprite_group_left(
                sprite_group,
                left + weights[index][0] + offset
            )
            width = bounding_box(sprite_group).width
            offset += weights[index][0] + width + weights[index][1]
