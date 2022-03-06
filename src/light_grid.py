from texture_manager import TextureManager
from ui import SpriteElement
from pygame.sprite import Group
from pygame import Vector2


class LightGrid:
    def __init__(self, level_manager):
        self.level_manager = level_manager
        self.texture_id = TextureManager.add_texture(
            "../resources/spr_light_grid.png")
        self.texture = TextureManager.get_texture(self.texture_id)
        self.light_grid_group = Group()
        self.construct()

    def construct(self):
        cols = self.level_manager.width // self.texture.get_width()
        rows = self.level_manager.height // self.texture.get_height()
        for row in range(rows):
            for col in range(cols):
                x = row * self.texture.get_width()
                y = col * self.texture.get_height()
                SpriteElement(
                    (x, y),
                    [self.light_grid_group],
                    self.texture.copy()
                )

    def update(self, player):
        for sprite in self.light_grid_group:
            tile_alpha = 255
            sprite_pos = Vector2(sprite.rect.center)
            distance = sprite_pos.distance_to(player.rect.center)

            if distance < 200:
                tile_alpha = 0
            else:
                tile_alpha = (51 * (distance - 200)) / 10

            for torch in self.level_manager.toches:
                distance = sprite_pos.distance_to(torch.rect.center)
                if distance < 100:
                    tile_alpha -= (tile_alpha -
                                   ((tile_alpha / 100) * distance)) * 30

            if tile_alpha < 0:
                tile_alpha = 0

            sprite.image.set_alpha(tile_alpha)

    def render(self, renderer):
        for sprite in self.light_grid_group:
            renderer.render(sprite)
