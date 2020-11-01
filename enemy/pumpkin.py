from entity import Entity


class Pumpkin(Entity):
    def __init__(self, position, sprite_key='pumpkin_1'):
        super(Pumpkin, self).__init__(position, sprite_key, name='pumpkin', hp=5, max_hp=5)
        self.breaking_level = 0

    def draw(self, surface):
        surface.blit(self.sprite.get_current_frame(), self.rect)

    def damage(self, damage_count):
        self.breaking_level += 1
        if self.breaking_level > 4:
            self.hp = 0
            self.alive = False
        else:
            self.sprite = self.sprites[f'pumpkin_{self.breaking_level + 1}']
