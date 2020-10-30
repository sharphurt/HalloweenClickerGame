import pygame as pg

from healthbar import HealthBar
from entity import Entity


class Ghost(Entity):
    def __init__(self, position, sprite_key):
        self.position = position

        super(Ghost, self).__init__(position, sprite_key, name='ghost', hp=100, max_hp=100)
        self.healthbar = HealthBar(self)

    def draw(self, surface):
        surface.blit(self.sprite.get_current_frame(), self.rect)
        self.healthbar.draw(surface)
