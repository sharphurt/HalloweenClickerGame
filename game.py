import pygame as pg

from Difficulty import Difficulty
from constants import *
from display import Display
from enemy.ghost import Ghost
from enemy.pumpkin import Pumpkin
from player import Player
import random as rnd

from sprite import Sprite


class Game:
    def __init__(self):
        pg.init()
        self.display = Display(pg.image.load('assets/background.jpg'))
        self.player = None
        self.enemies = []
        self.pumpkins = []
        self.create_entities()
        self.clock = pg.time.Clock()
        self.running = True
        self.NEW_GHOST = pg.USEREVENT
        self.NEW_PUMPKIN = pg.USEREVENT + 1
        pg.time.set_timer(self.NEW_GHOST, 3000)
        pg.time.set_timer(self.NEW_PUMPKIN, 3000)
        self.difficulty = Difficulty.EASY
        self.kills_count = 0
        self.player_movement = None

    def create_entities(self):
        self.enemies = [
            Ghost((rnd.randint(-200, 0), rnd.randint(0, self.display.HEIGHT // 4))),
            Pumpkin((WIDTH // 2, -100), 'pumpkin_1')
        ]
        self.player = Player((self.display.WIDTH / 2, self.display.HEIGHT - 200), 'player_stand')

    def check_collision(self):
        [self.player.damage(1) for e in self.enemies if self.player.check_collision(e)]

    def run_events(self):
        for event in pg.event.get():
            if event.type == self.NEW_GHOST:
                self.create_new_enemies_wave(Ghost)
            if event.type == self.NEW_PUMPKIN:
                self.create_new_enemies_wave(Pumpkin)
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONUP:
                clicked_enemies = self.get_enemies_under_cursor(pg.mouse.get_pos())
                self.process_damage(clicked_enemies, 1)
            if event.type == pg.KEYUP:
                self.player.sprite = self.player.sprites['player_stand']

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.player_movement = ((1, 0), 2)
        if keys[pg.K_LEFT]:
            self.player_movement = ((-1, 0), 2)

    def update(self):
        if self.player_movement is not None:
            self.player.update(offset=self.player_movement, sprite=self.player.sprites['player_run'])
            self.player_movement = None
        for enemy in self.enemies:
            if isinstance(enemy, Ghost):
                enemy.update(dest=(self.player.rect.center, 2))
            elif isinstance(enemy, Pumpkin):
                enemy.update(offset=((0, 1), 2))

    def create_new_enemies_wave(self, enemy):
        for i in range(rnd.randint(0, self.difficulty.value * 3)):
            x = -100 if rnd.randint(0, 100) % 2 == 0 else WIDTH + 100
            self.enemies.append(enemy((x, 0)))

    def get_enemies_under_cursor(self, pos):
        enemies_under_cursor = []
        for e in self.enemies:
            if e.rect.collidepoint(pos):
                enemies_under_cursor.append(e)
        return enemies_under_cursor

    def process_damage(self, enemies, damage):
        for e in enemies:
            e.damage(damage)
            if not e.alive:
                self.kills_count += 1
                self.enemies.remove(e)

    def game_over(self):
        pg.display.set_caption('Game Over')
        self.running = True
        self.create_entities()
        self.run()

    def run(self):
        while self.running:
            self.run_events()
            self.update()
            self.check_collision()

            self.display.draw(self.player, *self.enemies, *self.pumpkins)

            pg.display.set_caption(f'FPS: {self.clock.get_fps()}')
            if not self.player.alive:
                self.running = False

            self.clock.tick(FPS)
        self.game_over()
