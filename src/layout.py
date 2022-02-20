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


def compute_max_row_heights(sprite_groups, cols, rows):
    """Return dict of max height indexed by row"""
    max_row_heights = defaultdict(lambda: 0)
    for col in range(cols):
        for row in range(rows):
            index = col + row * cols
            if index >= len(sprite_groups):
                continue
            sprite_group = sprite_groups[index]
            height = bounding_box(sprite_group).height
            max_row_heights[row] = max(max_row_heights[row], height)

    return max_row_heights


def compute_max_row_height(sprite_groups):
    """Return max sprite_group height"""
    max_row_heights = compute_max_row_heights(
        sprite_groups,
        1,
        len(sprite_groups)
    )
    return max(max_row_heights.values())


def screen_rect():
    display_surface = pygame.display.get_surface()
    return display_surface.get_rect()


# -----------------
# Layout Algorithms
# -----------------
def move(sprites, x, y):
    """Move sprites by x and y"""
    sprite_groups = convert_to_sprite_groups(sprites)
    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.left += x
            sprite.rect.top += y


def justify_left(sprites, target):
    """Align left of sprites global bounding box with left of target."""
    sprite_groups = convert_to_sprite_groups(sprites)
    bbox = global_bounding_box(sprite_groups)

    try:
        offset = target.left - bbox.left
    except AttributeError:
        offset = target - bbox.left

    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.left += offset


def justify_top(sprites, target):
    """Align top of sprites global bounding box with top of target."""
    sprite_groups = convert_to_sprite_groups(sprites)
    bbox = global_bounding_box(sprite_groups)

    try:
        offset = target.top - bbox.top
    except AttributeError:
        offset = target - bbox.top

    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.top += offset


def justify_right(sprites, target):
    """Align right of sprites global bounding box with right of target."""
    sprite_groups = convert_to_sprite_groups(sprites)
    bbox = global_bounding_box(sprite_groups)

    try:
        offset = target.right - bbox.width
    except AttributeError:
        offset = target - bbox.width

    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.left += offset


def justify_bottom(sprites, target):
    """Align bottom of sprites global bounding box with bottom of target."""
    sprite_groups = convert_to_sprite_groups(sprites)
    bbox = global_bounding_box(sprite_groups)

    try:
        offset = target.bottom - bbox.height
    except AttributeError:
        offset = target - bbox.height

    for sprite_group in sprite_groups:
        for sprite in sprite_group:
            sprite.rect.bottom += offset


def position_sprite_group_left(sprite_group, value):
    """Position left side of sprite_group bbox by value."""
    bbox = bounding_box(sprite_group)
    for sprite in sprite_group:
        offsetx = sprite.rect.left - bbox.left
        sprite.rect.left = value + offsetx


def position_sprite_group_top(sprite_group, value):
    """Position top side of sprite_group bbox by value."""
    bbox = bounding_box(sprite_group)
    for sprite in sprite_group:
        offsety = sprite.rect.top - bbox.top
        sprite.rect.top = value + offsety


def stack_hort(sprites, cols=None, weights=None):
    """Stack sprites next to each other from right to left seperated by weights."""
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


def stack_vert(sprites, cols=None, weights=None, seperator=0, distribute_evenly=False):
    """Stack sprites next to each other from top to bottom seperated by weights and or seperator."""
    sprite_groups = convert_to_sprite_groups(sprites)
    cols = len(sprite_groups) if cols is None else cols
    rows = math.ceil(len(sprite_groups)/cols)
    weights = normalize_weights(weights)
    max_row_height = compute_max_row_height(sprite_groups)
    max_row_heights = compute_max_row_heights(sprite_groups, cols, rows)

    # update weights by seperator
    for row in range(rows):
        if row == 0:
            continue
        weights[row] = max(weights[row], seperator)

    # compute spacer
    spacers = defaultdict(lambda: [0, 0])
    for col in range(cols):
        for row in range(rows):
            index = col + row * cols
            if index >= len(sprite_groups):
                continue

            if distribute_evenly:
                row_height = max_row_height
            else:
                row_height = max_row_heights[row]
            sprite_group = sprite_groups[index]
            space = row_height - bounding_box(sprite_group).height
            spacers[index][0] = space/2
            spacers[index][1] = space/2

    # layout
    top = global_bounding_box(sprite_groups).top
    for col in range(cols):
        offset = 0
        for row in range(rows):
            index = col + row * cols
            if index >= len(sprite_groups):
                continue
            sprite_group = sprite_groups[index]
            space = weights[row] + spacers[index][0]
            position_sprite_group_top(
                sprite_group,
                top + space + offset
            )
            height = bounding_box(sprite_group).height
            offset += space + height + spacers[index][1]

    # # layout
    # top = global_bounding_box(sprite_groups).top
    # for col in range(cols):
    #     offset = 0
    #     for row in range(rows):
    #         index = col + row * cols
    #         if index >= len(sprite_groups):
    #             continue
    #         sprite_group = sprite_groups[index]
    #         offset += weights[row]
    #         position_sprite_group_top(sprite_group, top + offset)
    #         offset += max_row_heights[row]


def distribute_vert(sprites, cols=None, span=0):
    """Evenly distribute sprites vertically relative to their global bounding box."""

    # implement in terms of stack_vert

    # sprite_groups = convert_to_sprite_groups(sprites)
    # cols = len(sprite_groups) if cols is None else cols
    # rows = math.ceil(len(sprite_groups)/cols)
    # max_row_height = max(compute_max_row_height(sprite_groups), span)

    # # layout
    # weights = defaultdict(lambda: [0, 0])
    # for col in range(cols):
    #     for row in range(rows):
    #         index = col + row * cols
    #         if index >= len(sprite_groups):
    #             continue
    #         sprite_group = sprite_groups[index]
    #         space = max_row_height - bounding_box(sprite_group).height
    #         weights[index][0] = space/2
    #         weights[index][1] = space/2

    # top = global_bounding_box(sprite_groups).top
    # for col in range(cols):
    #     offset = 0
    #     for row in range(rows):
    #         index = col + row * cols
    #         if index >= len(sprite_groups):
    #             continue
    #         sprite_group = sprite_groups[index]
    #         position_sprite_group_top(
    #             sprite_group,
    #             top + weights[index][0] + offset
    #         )
    #         height = bounding_box(sprite_group).height
    #         offset += weights[index][0] + height + weights[index][1]
