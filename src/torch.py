from texture_manager import TextureManager
from game_object import GameObject


class Torch(GameObject):
    def __init__(self, position, groups):
        super().__init__(groups)
        texture_id = TextureManager.add_texture("../resources/spr_torch.png")
        self.image = TextureManager.get_texture(texture_id)
        self.rect = self.image.get_rect(center=position)
