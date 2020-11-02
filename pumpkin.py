from constants import HEIGHT
from entity.entity import Entity


class Pumpkin(Entity):
    def __init__(self, position, sprite_key='pumpkin'):
        super(Pumpkin, self).__init__(position, sprite_key, name='pumpkin', hp=5, max_hp=5)
        self.position = position
        self.breaking_level = 0

    def draw(self, surface):
        surface.blit(self.sprite.get_current_frame(), self.rect)

    def update(self, dest=None, offset=None, sprite=None):
        super(Pumpkin, self).update(dest, offset, sprite)
        _, y = self.position
        if y >= HEIGHT - 100:
            self.kill()
