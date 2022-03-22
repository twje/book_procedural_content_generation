from random import randint

from pygame import Vector2
from entity import Entity


class Enemy(Entity):
    def __init__(self, groups):
        super().__init__(groups)
        self.health = randint(80, 120)
        self.attack = randint(6, 10)
        self.defence = randint(6, 10)
        self.stemina = randint(6, 10)
        self.dexterity = randint(6, 10)
        self.stemina = randint(6, 10)
        self.speed = randint(150, 200)

    def take_demage(self, demage):
        self.health -= demage

    def is_dead(self):
        return self.health <= 0

    @property
    def position(self):
        return Vector2(self.rect.center)
