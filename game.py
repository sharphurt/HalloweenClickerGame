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
        self.player = Player((self.display.WIDTH / 2, self.display.HEIGHT - 200), 'player_static_stand')
        self.enemies = [Ghost((rnd.randint(0, self.display.WIDTH), rnd.randint(0, self.display.HEIGHT)), 'ghost_fly')
                        for _ in range(5)]
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.display.draw(self.player, *self.enemies)
            for event in pg.event.get():
                if event.type is pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    [e.damage(10) for e in self.enemies if e.rect.collidepoint(pos)]

            [self.enemies.remove(e) for e in self.enemies if not e.alive]
            pg.display.set_caption(str(int(self.clock.get_fps())))
            self.clock.tick(FPS)

        pg.quit()
        exit()
