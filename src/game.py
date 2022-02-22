from texture_manager import TextureManager
from state_machine import StateMachine
from playing_state import PlayingState
from settings import *
from support import *
import groups
import layout
import ui
import pygame


class Game:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.ui_sprites = pygame.sprite.Group()
        self.ui_debug_sprites = groups.BoundingBoxUIDebugGroup()

        self.load_ui()
        self.state_machine = StateMachine()
        self.state_machine.add_state(GAME_STATE.PLAYING, PlayingState(self))
        self.state_machine.set_state(GAME_STATE.PLAYING)

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

        # coin and gem
        text_width = 100
        self.coin_ui_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.load_texture("../resources/ui/spr_coin_ui.png", 0.75)
        )
        top_sprites.append(self.coin_ui_sprite)

        self.coin_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites],
            "000000",
            min_width=text_width
        )
        top_sprites.append(self.coin_ui_text)

        self.gem_ui_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.load_texture("../resources/ui/spr_gem_ui.png", 0.75)
        )
        top_sprites.append(self.gem_ui_sprite)

        self.gem_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites],
            "000000",
            min_width=text_width,
        )
        top_sprites.append(self.gem_ui_text)

        # key
        self.key_ui_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.load_texture("../resources/ui/spr_key_ui.png", 0.75)
        )
        bottom_sprites.append(self.key_ui_sprite)

        # stats
        text_width = 30
        self.attack_stat_textures = [
            self.load_texture("../resources/ui/spr_attack_ui.png"),
            self.load_texture("../resources/ui/spr_attack_ui_alt.png")
        ]
        self.attack_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.attack_stat_textures[0]
        )
        bottom_sprites.append(self.attack_stat_sprite)

        self.attack_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites],
            "10",
            min_width=text_width,
        )
        bottom_sprites.append(self.attack_ui_text)

        self.defence_stat_textures = [
            self.load_texture("../resources/ui/spr_defense_ui.png"),
            self.load_texture("../resources/ui/spr_defense_ui_alt.png")
        ]
        self.defence_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.defence_stat_textures[0]
        )
        bottom_sprites.append(self.defence_stat_sprite)

        self.defence_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites],
            "10",
            min_width=text_width,
        )
        bottom_sprites.append(self.defence_ui_text)

        self.strength_stat_textures = [
            self.load_texture("../resources/ui/spr_strength_ui.png"),
            self.load_texture("../resources/ui/spr_strength_ui_alt.png")
        ]
        self.strength_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.strength_stat_textures[0]
        )
        bottom_sprites.append(self.strength_stat_sprite)

        self.strength_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites],
            "10",
            min_width=text_width,
        )
        bottom_sprites.append(self.strength_ui_text)

        self.dexterity_stat_textures = [
            self.load_texture("../resources/ui/spr_dexterity_ui.png"),
            self.load_texture("../resources/ui/spr_dexterity_ui_alt.png")
        ]
        self.dexterity_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.dexterity_stat_textures[0]
        )
        bottom_sprites.append(self.dexterity_stat_sprite)

        self.dexterity_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites],
            "10",
            min_width=text_width,
        )
        bottom_sprites.append(self.dexterity_ui_text)

        self.stamina_stat_textures = [
            self.load_texture("../resources/ui/spr_stamina_ui.png"),
            self.load_texture("../resources/ui/spr_stamina_ui_alt.png")
        ]
        self.stamina_stat_sprite = ui.SpriteElement(
            (0, 0),
            [self.ui_sprites],
            self.stamina_stat_textures[0]
        )
        bottom_sprites.append(self.stamina_stat_sprite)

        self.stamina_ui_text = ui.TextElement(
            (0, 0),
            [self.ui_sprites],
            "10",
            min_width=text_width,
        )
        bottom_sprites.append(self.stamina_ui_text)

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
        top_rect = pygame.rect.Rect(top_sprites[0].rect)
        for top_sprite in top_sprites:
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
        bottom_rect = pygame.rect.Rect(bottom_sprites[0].rect)
        for bottom_sprite in bottom_sprites:
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
