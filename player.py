from healthbar import HealthBar
from entity import Entity


class Player(Entity):
    def __init__(self, position, sprite_key):
        super(Player, self).__init__(position, sprite_key, name='player', hp=100, max_hp=100)
        self.healthbar = HealthBar(self)

    def draw(self, surface):
        surface.blit(self.sprite.get_current_frame(), self.rect)
        self.healthbar.draw(surface)
