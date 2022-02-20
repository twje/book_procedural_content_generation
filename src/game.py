from traceback import print_tb
from level import Level
from player import Player
from texture_manager import TextureManager
from settings import *
from support import *
import groups
import layout
import ui
import pygame


class GridUI:
    def __init__(self, data, cols, groups):
        self.data = data
        self.packed_data = [self.data[i:i+cols]
                            for i in range(0, len(self.data), cols)]
        self.cols = cols
        self.groups = groups

    def left_justify(self, indicies):
        #foo = layout.HortStack(self.data, 4)
        #foo.distribute(150, 0)
        # foo.layout()

        layout.distribute_hort(self.data, cols=4)

        #layout.distribute_hort(self.data, 4, 0, layout.Direction.CENTER)
        #layout.expand_hort(self.data, 4, 500)

        #
        # layout.align_middle_vert(*self.data)

        # left justify sprites in each row
        # for row in self.packed_data:
        #layout.move(0, 0, *self.data)

        #layout.move(300, 300,self.data)

        # layout.stack_hort(
        #     self.data,
        #     cols=4,
        #     space=10,
        #     weights=5
        # )

        # layout.stack_vert(
        #     self.data,
        #     cols=4,
        #     weights=5
        # )

        # bounds.run()

        #ui.Box(bounds, self.groups)
        #ui.Box(pygame.rect.Rect(0, 0, 500, 200), self.groups)

        # stack rows on top of each other
        # layout.stack_vert(
        #     self.packed_data,
        # )

    def __iter__(self):
        return iter(self.data)


class HelpUI:
    def __init__(self, groups):
        self.groups = groups
        self.col1 = []
        self.all_sprites = []
        self.hort_space = 10

    def show(self):
        postion = (0, 0)
        col0_unpack = [
            self.load_sprite_element(
                "../resources/ui/spr_attack_ui.png"),
            self.load_text_element("Attack"),
            self.load_sprite_element(
                "../resources/ui/spr_attack_ui_alt.png"),
            self.load_text_element("Attack"),
            self.load_sprite_element("../resources/ui/spr_defense_ui.png"),
            self.load_text_element("Defence"),
            self.load_sprite_element("../resources/ui/spr_defense_ui_alt.png"),
            self.load_text_element("Defence"),
            self.load_sprite_element("../resources/ui/spr_strength_ui.png"),
            self.load_text_element("Strength"),
            self.load_sprite_element(
                "../resources/ui/spr_strength_ui_alt.png"),
            self.load_text_element("Strength"),
            self.load_sprite_element("../resources/ui/spr_dexterity_ui.png"),
            self.load_text_element("Dexterity"),
            self.load_sprite_element(
                "../resources/ui/spr_dexterity_ui_alt.png"),
            self.load_text_element("Dexterity"),

            self.load_sprite_element("../resources/ui/spr_stamina_ui.png"),
            self.load_text_element("Stamina"),
            self.load_sprite_element("../resources/ui/spr_stamina_ui_alt.png"),
            self.load_text_element("Stamina"),
        ]

        grid = GridUI(col0_unpack, 4, self.groups)
        grid.left_justify({1: 15, 2: 0, 3: 0})

        #col0 = [col0_unpack[i:i+2] for i in range(0, len(col0_unpack), 2)]

        # layout.align_middle_vert(*col0_unpack)
        # layout.left_justify(col0, 15)
        # layout.stack_vert(
        #     0,
        #     *col0,
        #     rules=[layout.stack_vert_evenly_justify_rule]
        # )

        # self.col1.append([
        #     self.load_sprite_element("../resources/ui/spr_attack_ui_alt.png"),
        #     self.load_text_element("Attack Power Up")
        # ])
        # self.col1.append([
        #     self.load_sprite_element("../resources/ui/spr_defense_ui_alt.png"),
        #     self.load_text_element("Defence Power Up")
        # ])
        # self.col1.append([
        #     self.load_sprite_element("../resources/ui/spr_strength_ui_alt.png"),
        #     self.load_text_element("Strength Power Up")
        # ])
        # self.col1.append([
        #     self.load_sprite_element("../resources/ui/spr_dexterity_ui_alt.png"),
        #     self.load_text_element("Dexterity Power Up")
        # ])
        # self.col1.append([
        #     self.load_sprite_element("../resources/ui/spr_stamina_ui_alt.png"),
        #     self.load_text_element("Stamina Power Up")
        # ])

    def hide(self):
        pass

    # --------------
    # Helper Methods
    # --------------
    def load_sprite_element(self, filepath, scale=1, position=(0, 0)):
        return ui.SpriteElement(
            position,
            self.groups,
            self.load_texture(filepath, scale)
        )

    def load_text_element(self, text, position=(0, 0)):
        return ui.TextElement(
            position,
            self.groups,
            text
        )

    def load_texture(self, filepath, scale):
        texture_id = TextureManager.add_texture(filepath)
        texture = TextureManager.get_texture(texture_id)
        if scale != 1:
            dimension = pygame.Vector2(texture.get_rect().size) * scale
            texture = pygame.transform.scale(texture, dimension)
        return texture


class Game:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = groups.YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()
        self.ui_debug_sprites = groups.BoundingBoxUIDebugGroup()

        self.level = Level(self.visible_sprites, self.obstacle_sprites)

        self.player = Player(
            (TILE_SIZE, TILE_SIZE),
            [self.visible_sprites],
            self.obstacle_sprites
        )

        self.help_ui = HelpUI([self.ui_sprites, self.ui_debug_sprites])
        self.help_ui.show()

        # self.load_ui()

    def load_ui(self):
        top_sprites = []
        bottom_sprites = []

        # player UI sprite
        self.player_ui_sprite = self.load_sprite_element(
            "../resources/ui/spr_warrior_ui.png",
            [self.ui_sprites]
        )
        top_sprites.append(self.player_ui_sprite)

        # bar outlines
        self.health_bar_outline_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.load_texture("../resources/ui/spr_bar_outline.png")
        )
        top_sprites.append(self.health_bar_outline_sprite)

        self.mana_bar_outline_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.load_texture("../resources/ui/spr_bar_outline.png")
        )
        top_sprites.append(self.mana_bar_outline_sprite)

        # bars
        self.health_bar_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.load_texture("../resources/ui/spr_health_bar.png")
        )
        top_sprites.append(self.health_bar_sprite)

        self.mana_bar_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.load_texture("../resources/ui/spr_mana_bar.png")
        )
        top_sprites.append(self.mana_bar_sprite)

        # # coin and gem
        # text_width = 100
        # self.coin_ui_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.load_texture("../resources/ui/spr_coin_ui.png", 0.75)
        # )
        # top_sprites.append(self.coin_ui_sprite)

        # self.coin_ui_text = ui.TextElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     "000000",
        #     min_width=text_width
        # )
        # top_sprites.append(self.coin_ui_text)

        # self.gem_ui_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.load_texture("../resources/ui/spr_gem_ui.png", 0.75)
        # )
        # top_sprites.append(self.gem_ui_sprite)

        # self.gem_ui_text = ui.TextElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     "000000",
        #     min_width=text_width,
        # )
        # top_sprites.append(self.gem_ui_text)

        # # key
        # self.key_ui_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.load_texture("../resources/ui/spr_key_ui.png", 0.75)
        # )
        # bottom_sprites.append(self.key_ui_sprite)

        # # stats
        # text_width = 30
        # self.attack_stat_textures = [
        #     self.load_texture("../resources/ui/spr_attack_ui.png"),
        #     self.load_texture("../resources/ui/spr_attack_ui_alt.png")
        # ]
        # self.attack_stat_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.attack_stat_textures[0]
        # )
        # bottom_sprites.append(self.attack_stat_sprite)

        # self.attack_ui_text = ui.TextElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     "10",
        #     min_width=text_width,
        # )
        # bottom_sprites.append(self.attack_ui_text)

        # self.defence_stat_textures = [
        #     self.load_texture("../resources/ui/spr_defense_ui.png"),
        #     self.load_texture("../resources/ui/spr_defense_ui_alt.png")
        # ]
        # self.defence_stat_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.defence_stat_textures[0]
        # )
        # bottom_sprites.append(self.defence_stat_sprite)

        # self.defence_ui_text = ui.TextElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     "10",
        #     min_width=text_width,
        # )
        # bottom_sprites.append(self.defence_ui_text)

        # self.strength_stat_textures = [
        #     self.load_texture("../resources/ui/spr_strength_ui.png"),
        #     self.load_texture("../resources/ui/spr_strength_ui_alt.png")
        # ]
        # self.strength_stat_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.strength_stat_textures[0]
        # )
        # bottom_sprites.append(self.strength_stat_sprite)

        # self.strength_ui_text = ui.TextElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     "10",
        #     min_width=text_width,
        # )
        # bottom_sprites.append(self.strength_ui_text)

        # self.dexterity_stat_textures = [
        #     self.load_texture("../resources/ui/spr_dexterity_ui.png"),
        #     self.load_texture("../resources/ui/spr_dexterity_ui_alt.png")
        # ]
        # self.dexterity_stat_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.dexterity_stat_textures[0]
        # )
        # bottom_sprites.append(self.dexterity_stat_sprite)

        # self.dexterity_ui_text = ui.TextElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     "10",
        #     min_width=text_width,
        # )
        # bottom_sprites.append(self.dexterity_ui_text)

        # self.stamina_stat_textures = [
        #     self.load_texture("../resources/ui/spr_stamina_ui.png"),
        #     self.load_texture("../resources/ui/spr_stamina_ui_alt.png")
        # ]
        # self.stamina_stat_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     self.stamina_stat_textures[0]
        # )
        # bottom_sprites.append(self.stamina_stat_sprite)

        # self.stamina_ui_text = ui.TextElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     "10",
        #     min_width=text_width,
        # )
        # bottom_sprites.append(self.stamina_ui_text)

        # top left layout
        health_bar = [
            self.health_bar_outline_sprite,
            self.health_bar_sprite,
        ]
        mana_bar = [
            self.mana_bar_outline_sprite,
            self.mana_bar_sprite
        ]
        bars = [*health_bar, *mana_bar]

        layout.align_middle_hort(bars)
        layout.align_middle_vert(bars)

        layout.right_justify(health_bar, pygame.Rect(100, 100, 200, 200))

        # layout.stack_vert([health_bar, mana_bar])  # fix
        #layout.stack_hort([self.player_ui_sprite, bars], 10)
        #layout.align_middle_vert([self.player_ui_sprite, bars])
        # layout.move(10, 10, self.player_ui_sprite, bars)

        # # top center layout
        # inventory = [
        #     self.coin_ui_sprite,
        #     self.coin_ui_text,
        #     self.gem_ui_sprite,
        #     self.gem_ui_text
        # ]

        # layout.align_middle_vert(*inventory)
        # layout.stack_hort(10, *inventory)
        # layout.center_screen_hort(*inventory)
        # layout.move(0, 10, *inventory)

        # # bottom center layout
        # stats = [
        #     self.attack_stat_sprite,
        #     self.attack_ui_text,
        #     self.defence_stat_sprite,
        #     self.defence_ui_text,
        #     self.strength_stat_sprite,
        #     self.strength_ui_text,
        #     self.dexterity_stat_sprite,
        #     self.dexterity_ui_text,
        #     self.stamina_stat_sprite,
        #     self.stamina_ui_text,
        # ]

        # layout.stack_hort(5, *stats)
        # layout.align_middle_vert(*stats)
        # layout.bottom_screen_justify(*stats)
        # layout.center_screen_hort(*stats)
        # layout.move(0, -10, *stats)

        # # bottom right layout
        # layout.right_screen_justify(self.key_ui_sprite)
        # layout.bottom_screen_justify(self.key_ui_sprite)

        # # top strip
        # top_rect = pygame.rect.Rect(top_sprites[0].rect)
        # for top_sprite in top_sprites:
        #     top_rect = top_rect.union(top_sprite.rect)

        # top_ui_strip_texture = pygame.Surface(
        #     (self.display_surface.get_width(), top_rect.top + top_rect.height),
        #     pygame.SRCALPHA,
        #     32
        # )
        # top_ui_strip_texture.fill((255, 255, 255, 25))
        # self.top_ui_strip_sprite = ui.SpriteElement(
        #     (0, 0),
        #     [self.ui_sprites],
        #     top_ui_strip_texture
        # )

        # # bottom strip
        # bottom_rect = pygame.rect.Rect(bottom_sprites[0].rect)
        # for bottom_sprite in bottom_sprites:
        #     bottom_rect = bottom_rect.union(bottom_sprite.rect)

        # bottom_ui_strip_texture = pygame.Surface(
        #     (self.display_surface.get_width(), bottom_rect.height),
        #     pygame.SRCALPHA,
        #     32
        # )
        # bottom_ui_strip_texture.fill((255, 255, 255, 25))
        # self.bottom_ui_strip_sprite = ui.SpriteElement(
        #     (0, bottom_rect.top),
        #     [self.ui_sprites],
        #     bottom_ui_strip_texture
        # )

    def run(self):
        self.player.update()
        self.visible_sprites.custom_draw(self.player)
        self.ui_sprites.draw(self.display_surface)
        self.ui_debug_sprites.custom_draw()

    # --------------
    # Helper Methods
    # --------------
    def load_sprite_element(self, filepath, groups):
        return ui.SpriteElement(
            (0, 0),
            groups,
            self.load_texture(filepath)
        )

    def load_texture(self, filepath, scale=1):
        texture_id = TextureManager.add_texture(filepath)
        texture = TextureManager.get_texture(texture_id)
        if scale != 1:
            dimension = pygame.Vector2(texture.get_rect().size) * scale
            texture = pygame.transform.scale(texture, dimension)
        return texture
