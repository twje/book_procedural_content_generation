from enemy import Enemy
from texture_manager import TextureManager
from animation import Animation
from settings import *


class Humanoid(Enemy):
    def __init__(self, position, groups):
        super().__init__(groups)

        # load textures
        self.texture_ids = {}
        anim_states = [
            (ANIMATION_STATE.WALK_UP.value,
             "../resources/enemies/skeleton/spr_skeleton_walk_up.png"),
            (ANIMATION_STATE.WALK_RIGHT.value,
             "../resources/enemies/skeleton/spr_skeleton_walk_right.png"),
            (ANIMATION_STATE.WALK_DOWN.value,
             "../resources/enemies/skeleton/spr_skeleton_walk_down.png"),
            (ANIMATION_STATE.WALK_LEFT.value,
             "../resources/enemies/skeleton/spr_skeleton_walk_left.png"),
            (ANIMATION_STATE.IDLE_UP.value,
             "../resources/enemies/skeleton/spr_skeleton_idle_up.png"),
            (ANIMATION_STATE.IDLE_RIGHT.value,
             "../resources/enemies/skeleton/spr_skeleton_idle_right.png"),
            (ANIMATION_STATE.IDLE_DOWN.value,
             "../resources/enemies/skeleton/spr_skeleton_idle_down.png"),
            (ANIMATION_STATE.IDLE_LEFT.value,
             "../resources/enemies/skeleton/spr_skeleton_idle_left.png")
        ]
        for anim_state in anim_states:
            self.texture_ids[anim_state[0]
                             ] = TextureManager.add_texture(anim_state[1])

          # init animation
        self.animation = Animation()

        for anim_state in anim_states[:4]:
            self.animation.add_sequence(
                anim_state[0],
                self.texture_ids[anim_state[0]],
                8,
                0.15
            )
        for anim_state in anim_states[-4:]:
            self.animation.add_sequence(
                anim_state[0],
                self.texture_ids[anim_state[0]],
                1,
                0
            )

        self.animation_sequence = ANIMATION_STATE.WALK_UP.value

        # init sprite
        self.animation.set_sequence(self.animation_sequence)
        self.image = self.animation.get_frame()
        self.rect = self.image.get_rect(topleft=position)
