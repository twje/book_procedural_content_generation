import pygame


class TextureManager:
    texture_id = 0
    textures = {}

    @classmethod
    def add_texture(cls, filepath):
        if filepath in cls.textures:
            return cls.textures[filepath][0]
        else:
            cls.texture_id += 1
            surface = pygame.image.load(filepath).convert_alpha()
            cls.textures[filepath] = (cls.texture_id, surface)

        return cls.texture_id

    @classmethod
    def remove_texture(cls, texture_id):
        pass

    @classmethod
    def get_texture(cls, texture_id):
        return next(entry[1][1] for entry in cls.textures.items() if entry[1][0] == texture_id)
