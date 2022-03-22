from animation import Animation
from texture_manager import TextureManager
from game_object import GameObject
from settings import ITEM_TYPE


class Gem(GameObject):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.animation = Animation()
        self.texture_id = TextureManager.add_texture(
            "../resources/loot/gem/spr_pickup_gem.png")
        self.animation.add_sequence(0, self.texture_id, 8, 0.15)
        self.animation.set_sequence(0)       
        self.image = self.animation.get_frame()
        self.rect = self.image.get_rect(center=position)
       
        self.typez = ITEM_TYPE.GEM
        self.value = 15
        self.debug = True

    def update(self):
        self.animation.update()
        self.image = self.animation.get_frame()
