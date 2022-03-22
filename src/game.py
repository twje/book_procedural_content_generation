from texture_manager import TextureManager
from state_machine import StateMachine
from playing_state import PlayingState
from settings import *
from support import *
import layout
import ui
import pygame


class Game:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.ui_sprites = pygame.sprite.Group()
        self.top_sprites = pygame.sprite.Group()
        self.bottom_sprites = pygame.sprite.Group()
        self.item_values = {
            ITEM_TYPE.GOLD: "000000",
            ITEM_TYPE.GEM: "000000",
        }
        self.stat_values = {
            STAT_TYPE.ATTACK: "00",
            STAT_TYPE.DEFENCE: "00",
            STAT_TYPE.DEXTERITY: "00",
            STAT_TYPE.SETMINA: "00",
            STAT_TYPE.STRENGTH: "00"
        }
        self.load_ui()

        self.state_machine = StateMachine()
        self.state_machine.add_state(GAME_STATE.PLAYING, PlayingState(self))
        self.state_machine.set_state(GAME_STATE.PLAYING)
        pygame.mouse.set_visible(False)

    def update_health_bar(self, percent):
        self.health_bar_sprite.set_width(percent)

    def update_mana_bar(self, percent):
        self.mana_bar_sprite.set_width(percent)

    def add_gold(self, amount):
        self.add_currency(ITEM_TYPE.GOLD, amount)

    def add_gem(self, amount):
        self.add_currency(ITEM_TYPE.GEM, amount)

    def get_stat(self, stat_type):
        return self.stat_values[stat_type]

    def set_stat(self, stat_type, value):
        self.stat_values[stat_type] = str(value).rjust(2, "0")

    def add_currency(self, currency_type, amount):
        value = int(self.item_values[currency_type]) + amount
        self.item_values[currency_type] = str(value).rjust(6, "0")
        self.reset_ui()

    def reset_ui(self):
        self.ui_sprites.empty()
        self.top_sprites.empty()
        self.bottom_sprites.empty()
        self.load_ui()

    def load_ui(self):
        # player UI sprite
        self.player_ui_sprite = self.load_sprite_element(
            "../resources/ui/spr_warrior_ui.png",
            [self.ui_sprites, self.top_sprites]
        )

        # bar outlines
        self.health_bar_outline_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.load_texture("../resources/ui/spr_bar_outline.png")
        )

        self.mana_bar_outline_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.load_texture("../resources/ui/spr_bar_outline.png")
        )

        # bars
        self.health_bar_sprite = ui.Bar(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.load_texture("../resources/ui/spr_health_bar.png")
        )
        self.health_bar_width = self.health_bar_sprite.image.get_width()

        self.mana_bar_sprite = ui.Bar(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.load_texture("../resources/ui/spr_mana_bar.png")
        )
        self.mana_bar_width = self.mana_bar_sprite.image.get_width()

        # coin and gem
        text_width = 100
        self.coin_ui_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.load_texture("../resources/ui/spr_coin_ui.png", 0.75)
        )

        self.coin_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.item_values[ITEM_TYPE.GOLD],
            min_width=text_width
        )

        self.gem_ui_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.load_texture("../resources/ui/spr_gem_ui.png", 0.75)
        )

        self.gem_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites, self.top_sprites],
            self.item_values[ITEM_TYPE.GEM],
            min_width=text_width,
        )

        # key
        self.key_ui_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.load_texture("../resources/ui/spr_key_ui.png", 0.75)
        )

        # stats
        text_width = 30
        self.attack_stat_textures = [
            self.load_texture("../resources/ui/spr_attack_ui.png"),
            self.load_texture("../resources/ui/spr_attack_ui_alt.png")
        ]
        self.attack_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.attack_stat_textures[0]
        )

        self.attack_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.stat_values[STAT_TYPE.ATTACK],
            min_width=text_width,
        )

        self.defence_stat_textures = [
            self.load_texture("../resources/ui/spr_defense_ui.png"),
            self.load_texture("../resources/ui/spr_defense_ui_alt.png")
        ]
        self.defence_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.defence_stat_textures[0]
        )

        self.defence_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.stat_values[STAT_TYPE.DEFENCE],
            min_width=text_width,
        )

        self.strength_stat_textures = [
            self.load_texture("../resources/ui/spr_strength_ui.png"),
            self.load_texture("../resources/ui/spr_strength_ui_alt.png")
        ]
        self.strength_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.strength_stat_textures[0]
        )

        self.strength_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.stat_values[STAT_TYPE.STRENGTH],
            min_width=text_width,
        )

        self.dexterity_stat_textures = [
            self.load_texture("../resources/ui/spr_dexterity_ui.png"),
            self.load_texture("../resources/ui/spr_dexterity_ui_alt.png")
        ]
        self.dexterity_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.dexterity_stat_textures[0]
        )

        self.dexterity_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.stat_values[STAT_TYPE.DEXTERITY],
            min_width=text_width,
        )

        self.stamina_stat_textures = [
            self.load_texture("../resources/ui/spr_stamina_ui.png"),
            self.load_texture("../resources/ui/spr_stamina_ui_alt.png")
        ]
        self.stamina_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.stamina_stat_textures[0]
        )

        self.stamina_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites, self.bottom_sprites],
            self.stat_values[STAT_TYPE.SETMINA],
            min_width=text_width,
        )

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
        layout.stack_vert([health_bar, mana_bar], cols=1, seperator=3)
        layout.align_middle_vert([self.player_ui_sprite, bars])
        layout.stack_hort([self.player_ui_sprite, bars], seperator=20)
        layout.move([self.player_ui_sprite, bars], 5, 5)

        # top center layout
        inventory = [
            self.coin_ui_sprite,
            self.coin_ui_text,
            self.gem_ui_sprite,
            self.gem_ui_text
        ]

        layout.align_middle_vert(inventory)
        layout.stack_hort(inventory)
        layout.center_hort(inventory, layout.screen_rect())
        layout.move(inventory, 0, 5)

        # bottom center layout
        stats = [
            self.attack_stat_sprite,
            self.attack_ui_text,
            self.defence_stat_sprite,
            self.defence_ui_text,
            self.strength_stat_sprite,
            self.strength_ui_text,
            self.dexterity_stat_sprite,
            self.dexterity_ui_text,
            self.stamina_stat_sprite,
            self.stamina_ui_text,
        ]

        layout.stack_hort(stats, seperator=10)
        layout.align_middle_vert(stats)
        layout.justify_bottom(stats, layout.screen_rect())
        layout.center_hort(stats, layout.screen_rect())
        layout.move(stats, 0, -10)

        # bottom right layout
        layout.justify_right([self.key_ui_sprite], layout.screen_rect())
        layout.justify_bottom([self.key_ui_sprite], layout.screen_rect())
        layout.move([self.key_ui_sprite], -5, -5)

        # top strip
        top_rect = pygame.rect.Rect(self.top_sprites.sprites()[0].rect)
        for top_sprite in self.top_sprites:
            top_rect = top_rect.union(top_sprite.rect)

        top_ui_strip_texture = pygame.Surface(
            (self.display_surface.get_width(), top_rect.top + top_rect.height),
            pygame.SRCALPHA,
            32
        )
        top_ui_strip_texture.fill((255, 255, 255, 25))
        self.top_ui_strip_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            top_ui_strip_texture
        )

        # bottom strip
        bottom_rect = pygame.rect.Rect(self.bottom_sprites.sprites()[0].rect)
        for bottom_sprite in self.bottom_sprites:
            bottom_rect = bottom_rect.union(bottom_sprite.rect)

        bottom_ui_strip_texture = pygame.Surface(
            (self.display_surface.get_width(), bottom_rect.top),
            pygame.SRCALPHA,
            32
        )
        bottom_ui_strip_texture.fill((255, 255, 255, 25))
        self.bottom_ui_strip_sprite = ui.SpriteElement(
            (0, bottom_rect.top),
            [self.ui_sprites],
            bottom_ui_strip_texture
        )

    def run(self):
        self.state_machine.update()
        self.state_machine.render()
        self.ui_sprites.draw(self.display_surface)

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
