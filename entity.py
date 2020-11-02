import pygame as pg
from sprite import load_sprites


class Entity(pg.sprite.Sprite):
    def __init__(self, position, sprite_key, name='enemy', hp=100, max_hp=100):
        super(Entity, self).__init__()
        self.sprites = load_sprites()
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

    def _moveto(self, dest_point, speed):
        player_vector = pg.math.Vector2(dest_point)
        self_vector = pg.math.Vector2(self.rect.center)
        towards = player_vector - self_vector
        if towards.magnitude() != 0:
            towards = (player_vector - self_vector).normalize() * speed
        self.rect.center = self_vector + towards

    def _move_steps(self, dir_vector, steps):
        for i in range(steps):
            x, y = self.rect.center
            dx, dy = dir_vector
            if dx >= 0:
                self.sprite.flip(False)
            else:
                self.sprite.flip(True)

            self.rect.centerx = x + dx
            self.rect.centery = y + dy

    def update(self, dest=None, offset=None, sprite=None):
        if dest is not None:
            dest_point, speed = dest
            self._moveto(dest_point, speed)
        if offset is not None:
            dir_vector, steps = offset
            self._move_steps(dir_vector, steps)
        if sprite is not None:
            self.sprite = sprite

    def kill(self):
        self.alive = False
