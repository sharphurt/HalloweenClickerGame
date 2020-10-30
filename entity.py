import pygame as pg

from sprite import Sprite


class Entity(pg.sprite.Sprite):
    def __init__(self, position, sprite_key, name='enemy', hp=100, max_hp=100):
        super(Entity, self).__init__()
        self.sprite = Sprite(Sprite.sprite_table[sprite_key])
        self.rect = pg.rect.Rect(position,
                                 (self.sprite.width * self.sprite.scale, self.sprite.height * self.sprite.scale))
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.alive = True

    def damage(self, damage_count):
        self.hp -= damage_count
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
