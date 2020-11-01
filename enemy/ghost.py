import pygame as pg

from healthbar import HealthBar
from entity import Entity


class Ghost(Entity):
    def __init__(self, position, sprite_key='ghost_fly'):
        super(Ghost, self).__init__(position, sprite_key, name='ghost', hp=5, max_hp=5)
        self.position = position
        self.healthbar = HealthBar(self)

    def draw(self, surface):
        surface.blit(self.sprite.get_current_frame(), self.rect)
        self.healthbar.draw(surface)
