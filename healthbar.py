from constants import *
from entity import Entity
import pygame as pg


class HealthBar:
    def __init__(self, parent_entity, length=100):
        if not isinstance(parent_entity, Entity):
            raise Exception('The passed object is not an instance of the Entity class')
        self.length = length
        self.parent_entity = parent_entity

    def draw(self, surface):
        filling = self.calculate_fill()
        px, py = self.parent_entity.rect.topleft
        rect = pg.rect.Rect(px, py - 20, 100, 5)
        filling_rect = pg.rect.Rect(px, py - 20, filling, 5)
        color = self.__get_color_from_percent(filling)
        pg.draw.rect(surface, WHITE, rect)
        pg.draw.rect(surface, color, filling_rect)

    def calculate_fill(self):
        percent = 100 * self.parent_entity.hp // self.parent_entity.max_hp
        return 100 * percent // self.length


    @staticmethod
    def __get_color_from_percent(percent):
        if percent > 50:
            return 41, 220, 112
        if percent > 20:
            return 220, 205, 41
        return 208, 65, 65
