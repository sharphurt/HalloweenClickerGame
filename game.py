import pygame as pg

from constants import *
from display import Display
from enemy.ghost import Ghost
from player import Player
import random as rnd


class Game:
    def __init__(self):
        pg.init()
        self.display = Display(pg.image.load('assets/background.jpg'))
        self.player = None
        self.enemies = []
        self.create_entities()
        self.clock = pg.time.Clock()
        self.running = True

    def create_entities(self):
        self.enemies = [
            Ghost((rnd.randint(-200, 0), rnd.randint(0, self.display.HEIGHT // 4)),
                  'ghost_fly') for _ in range(5)
        ]
        self.player = Player((self.display.WIDTH / 2, self.display.HEIGHT - 200), 'player_stand')

    def check_collision(self):
        [self.player.damage(1) for e in self.enemies if self.player.check_collision(e)]

    def check_input(self):
        for event in pg.event.get():
            if event.type is pg.QUIT:
                self.running = False
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                [e.damage(10) for e in self.enemies if e.rect.collidepoint(pos)]
            if event.type == pg.KEYUP:
                self.player.sprite = self.player.sprites['player_stand']

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.player.sprite = self.player.sprites['player_run']
            self.player.move_steps((1, 0), 2)
        if keys[pg.K_LEFT]:
            self.player.sprite = self.player.sprites['player_run']
            self.player.move_steps((-1, 0), 2)

        [e.moveto(self.player.rect.center, 2) for e in self.enemies]

    def game_over(self):
        pg.display.set_caption('Game Over')
        self.running = True
        self.create_entities()
        self.run()

    def run(self):
        while self.running:
            self.check_input()
            self.check_collision()
            self.display.draw(self.player, *self.enemies)
            pg.display.set_caption(f'FPS: {self.clock.get_fps()}')

            [self.enemies.remove(e) for e in self.enemies if not e.alive]
            if not self.player.alive:
                self.running = False

            self.clock.tick(FPS)
        self.game_over()
