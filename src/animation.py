from texture_manager import TextureManager
import pygame


class AnimationSequence:
    def __init__(self, texture_id, frames, frame_speed):
        self.surfaces = []
        self.frames = frames
        self.frame_speed = frame_speed
        self.frame_index = 0

        surface = TextureManager.get_texture(texture_id)
        width = surface.get_width()/frames
        height = surface.get_height()
        for frame in range(frames):
            rect = pygame.Rect(
                frame * width,
                0,
                width,
                height
            )
            sub_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            sub_surface.blit(surface, (0, 0), rect)
            self.surfaces.append(sub_surface)

    def update(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.surfaces):
            self.frame_index = 0

    def get_frame(self):
        return self.surfaces[int(self.frame_index)]


class Animation:
    def __init__(self):
        self.sequences = {}
        self.index = None

    def add_sequence(self, sequence_id, texture_id, frames, frame_speed):
        self.sequences[sequence_id] = AnimationSequence(
            texture_id,
            frames,
            frame_speed
        )

    def set_sequence(self, sequence_id):
        if self.index != sequence_id:
            sequence = self.sequences[sequence_id]
            sequence.frame_index = 0
            self.index = sequence_id

    def get_frame(self):
        return self.sequences[self.index].get_frame()

    def update(self):
        self.sequences[self.index].update()
