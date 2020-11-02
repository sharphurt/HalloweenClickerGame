from entity.entity import Entity


class Heart(Entity):
    def __init__(self, position, sprite_key='heart'):
        super(Heart, self).__init__(position, sprite_key, name='heart', hp=1, max_hp=1)
        self.position = position

    def draw(self, surface):
        surface.blit(self.sprite.get_current_frame(), self.rect)
