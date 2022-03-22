from game_object import GameObject
from settings import STAT_TYPE


class Entity(GameObject):
    def __init__(self, groups):
        super().__init__(groups)
        self.stats = {
            STAT_TYPE.ATTACK: 0,
            STAT_TYPE.DEFENCE: 0,
            STAT_TYPE.STRENGTH: 0,
            STAT_TYPE.DEXTERITY: 0,
            STAT_TYPE.SETMINA: 0
        }

    @property
    def attack(self):
        return self.stats[STAT_TYPE.ATTACK]

    @attack.setter
    def attack(self, value):
        self.stats[STAT_TYPE.ATTACK] = round(value)

    @property
    def defence(self):
        return self.stats[STAT_TYPE.DEFENCE]

    @defence.setter
    def defence(self, value):
        self.stats[STAT_TYPE.DEFENCE] = round(value)

    @property
    def strength(self):
        return self.stats[STAT_TYPE.STRENGTH]

    @strength.setter
    def strength(self, value):
        self.stats[STAT_TYPE.STRENGTH] = round(value)

    @property
    def dexterity(self):
        return self.stats[STAT_TYPE.DEXTERITY]

    @dexterity.setter
    def dexterity(self, value):
        self.stats[STAT_TYPE.DEXTERITY] = round(value)

    @property
    def stemina(self):
        return self.stats[STAT_TYPE.SETMINA]

    @stemina.setter
    def stemina(self, value):
        self.stats[STAT_TYPE.SETMINA] = round(value)
