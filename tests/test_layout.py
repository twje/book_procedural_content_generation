
import pygame
import layout
from pygame.rect import Rect


class Element:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)


def test_bounding_box():
    # setup
    e1 = Element(0, 0, 100, 100)
    e2 = Element(50, 50, 100, 100)
    bbox = layout.bounding_box([e1, e2])

    # test
    assert bbox.left == 0
    assert bbox.top == 0
    assert bbox.right == 150
    assert bbox.bottom == 150


def test_global_bounding_box():
    # setup
    e1 = Element(0, 0, 100, 100)
    e2 = Element(50, 50, 100, 100)
    bbox = layout.global_bounding_box([[e1], [e2]])

    # test
    assert bbox.left == 0
    assert bbox.top == 0
    assert bbox.right == 150
    assert bbox.bottom == 150


def test_convert_to_sprite_groups():
    # setup
    values = ['a', ['b', 'c']]
    values = layout.convert_to_sprite_groups(values)

    # test
    assert values[0] == ['a']
    assert values[1] == ['b', 'c']


def test_normalize_weights_single_value():
    # setup
    weights = layout.normalize_weights(10)

    # test
    assert weights[0] == 10


def test_normalize_weights_dict():
    # setup
    weights = layout.normalize_weights({0: 10, 2: 5})

    # test
    assert weights[0] == 10
    assert weights[1] == 0
    assert weights[2] == 5


def test_compute_max_col_widths():
    # setup
    sprite_groups = layout.convert_to_sprite_groups([
        Element(0, 0, 50, 100),
        Element(0, 0, 100, 100),
        Element(0, 0, 50, 100),
        Element(0, 0, 200, 100)
    ])
    max_col_widths = layout.compute_max_col_widths(sprite_groups, 2, 2)

    # test
    assert len(max_col_widths) == 2
    assert max_col_widths[0] == 50
    assert max_col_widths[1] == 200


def test_compute_max_col_width():
    # setup
    sprite_groups = layout.convert_to_sprite_groups([
        Element(0, 0, 50, 100),
        Element(0, 0, 100, 100),
        Element(0, 0, 60, 100),
        Element(0, 0, 200, 100)
    ])
    max_col_width = layout.compute_max_col_width(sprite_groups)

    # test
    assert max_col_width == 200


def test_justify_left():
    # setup
    target = pygame.rect.Rect(5, 0, 100, 100)
    e1 = Element(10, 0, 100, 100)
    e2 = Element(110, 0, 100, 100)
    e3 = Element(200, 0, 100, 100)
    layout.justify_left([[e1, e2], e3], target)

    # test
    assert e1.rect.left == 5
    assert e2.rect.left == 105
    assert e3.rect.left == 195


def test_justify_top():
    # setup
    target = pygame.rect.Rect(0, 5, 100, 100)
    e1 = Element(0, 10, 100, 100)
    e2 = Element(0, 110, 100, 100)
    e3 = Element(0, 200, 100, 100)
    layout.justify_top([[e1, e2], e3], target)

    # test
    assert e1.rect.top == 5
    assert e2.rect.top == 105
    assert e3.rect.top == 195


def test_justify_right():
    pass


def test_justify_bottom():
    pass


def test_position_sprite_group_left():
    # setup
    sprite_group = [
        Element(0, 0, 50, 100),
        Element(50, 0, 50, 100),
    ]
    layout.position_sprite_group_left(sprite_group, 50)

    # test
    assert sprite_group[0].rect.left == 50
    assert sprite_group[1].rect.left == 100


def test_stack_hort_single_row():
    # setup
    e1 = Element(0, 0, 100, 100)
    e2 = Element(0, 0, 100, 100)
    e3 = Element(0, 0, 100, 100)
    layout.stack_hort([e1, e2, e3])

    # test
    assert e1.rect.left == 0
    assert e2.rect.left == 100
    assert e3.rect.left == 200


def test_stack_hort_with_global_bbox_x_pos_greater_than_zero():
    # setup
    e1 = Element(10, 0, 100, 100)
    e2 = Element(20, 0, 100, 100)
    e3 = Element(20, 0, 100, 100)
    layout.stack_hort([e1, e2, e3])

    # test
    assert e1.rect.left == 10
    assert e2.rect.left == 110
    assert e3.rect.left == 210


def test_stack_hort_weights_and_global_bbox_x_pos_greater_than_zero():
    # setup
    e1 = Element(10, 0, 100, 100)
    e2 = Element(20, 0, 100, 100)
    e3 = Element(20, 0, 100, 100)
    layout.stack_hort([e1, e2, e3], weights={0: 10, 1: 20, 2: 30})

    # test
    assert e1.rect.left == 20
    assert e2.rect.left == 140
    assert e3.rect.left == 270


def test_stack_hort_weights():
    # setup
    e1 = Element(0, 0, 100, 100)
    e2 = Element(0, 0, 100, 100)
    e3 = Element(0, 0, 100, 100)
    layout.stack_hort([e1, e2, e3], weights={0: 10, 1: 20, 2: 30})

    # test
    assert e1.rect.left == 10
    assert e2.rect.left == 130
    assert e3.rect.left == 260


def test_stack_hort_weights_with_cols():
    # setup
    e1 = Element(0, 0, 50, 100)
    e2 = Element(0, 0, 70, 100)
    e3 = Element(0, 0, 60, 100)
    e4 = Element(0, 0, 80, 100)
    layout.stack_hort([e1, e2, e3, e4], cols=2, weights={0: 10, 1: 20})

    # test
    assert e1.rect.left == 10
    assert e2.rect.left == 90
    assert e3.rect.left == 10
    assert e4.rect.left == 90


def test_distribute_hort():
    # setup
    e1 = Element(0, 0, 50, 100)
    e2 = Element(0, 0, 200, 100)
    e3 = Element(0, 0, 50, 100)
    layout.distribute_hort([e1, e2, e3])

    # test
    assert e1.rect.left == 75
    assert e2.rect.left == 200
    assert e3.rect.left == 475


def test_distribute_hort_and_global_bbox_x_pos_greater_than_zero():
    # setup
    e1 = Element(10, 0, 50, 100)
    e2 = Element(20, 0, 200, 100)
    e3 = Element(30, 0, 50, 100)
    layout.distribute_hort([e1, e2, e3])

    # test
    assert e1.rect.left == 85
    assert e2.rect.left == 210
    assert e3.rect.left == 485


def test_distribute_hort_with_cols():
    # setup
    e1 = Element(0, 0, 50, 100)
    e2 = Element(0, 0, 200, 100)
    e3 = Element(0, 0, 50, 100)
    layout.distribute_hort([e1, e2, e3], cols=2)

    # test
    assert e1.rect.left == 75
    assert e2.rect.left == 200
    assert e3.rect.left == 75
