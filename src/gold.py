from texture_manager import TextureManager
from game_object import GameObject
from settings import ITEM_TYPE


class Gold(GameObject):
    def __init__(self, position, groups):
        super().__init__(groups)
        texture_id = TextureManager.add_texture(
            "../resources/loot/gold/spr_pickup_gold_medium.png")
        self.image = TextureManager.get_texture(texture_id)
        self.rect = self.image.get_rect(center=position)
        self.typez = ITEM_TYPE.GOLD
        self.value = 15
        self.debug = True
