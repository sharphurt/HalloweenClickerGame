import pygame as pg
from sprite import Sprite


class Entity(pg.sprite.Sprite):

    def __init__(self, position, sprite_key, name='enemy', hp=100, max_hp=100):
        super(Entity, self).__init__()
        self.sprites = {
            'player_stand': Sprite(Sprite.sprite_table['player_stand']),
            'player_run': Sprite(Sprite.sprite_table['player_run']),
            'ghost_fly': Sprite(Sprite.sprite_table['ghost_fly'])
        }

        self.sprite = self.sprites[sprite_key]
        self.rect = pg.rect.Rect(
            position,
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

    def check_collision(self, other):
        return self.rect.colliderect(other.rect)

    def moveto(self, dest_point, speed):
        player_vector = pg.math.Vector2(dest_point)
        self_vector = pg.math.Vector2(self.rect.center)
        towards = player_vector - self_vector
        if towards.magnitude() != 0:
            towards = (player_vector - self_vector).normalize() * speed
        self.rect.center = self_vector + towards

    def move_steps(self, dir_vector, steps):
        for i in range(steps):
            x, y = self.rect.center
            dx, dy = dir_vector
            if dx >= 0:
                self.sprite.flip(False)
            else:
                self.sprite.flip(True)

            self.rect.centerx = x + dx
            self.rect.centery = y + dy
