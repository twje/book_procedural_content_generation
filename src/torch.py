import imp
from secrets import randbelow


import random
from texture_manager import TextureManager
from game_object import GameObject
from animation import Animation


class Torch(GameObject):
    def __init__(self, position, groups):
        super().__init__(groups)
        texture_id = TextureManager.add_texture("../resources/spr_torch.png")
        self.animation = Animation()
        self.animation.add_sequence(0, texture_id, 5, 0.15)
        self.animation.set_sequence(0)
        self.image = self.animation.get_frame()
        self.rect = self.image.get_rect(center=position)
        self.brightness = 255

    def animate(self):
        self.animation.update()
        self.image = self.animation.get_frame()

    def update(self):
        self.animate()
        self.brightness = random.randint(100, 120) / 100
