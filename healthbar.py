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
        rect = pg.rect.Rect(px, py - 20, filling, 5)
        color = self.__get_color_from_percent(self.parent_entity.hp)
        pg.draw.rect(surface, color, rect)

    def calculate_fill(self):
        parent = self.parent_entity
        percent = parent.max_hp // 100 * parent.hp
        return self.length // 100 * percent


    @staticmethod
    def __get_color_from_percent(percent):
        if percent > 50:
            return 41, 220, 112
        if percent > 20:
            return 220, 205, 41
        return 208, 65, 65
