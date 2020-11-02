import pygame as pg

from Difficulty import Difficulty
from constants import *
from display import Display
from entity.ghost import Ghost
from pumpkin import Pumpkin
from entity.heart import Heart
from entity.player import Player
import random as rnd


class Game:
    def __init__(self):
        pg.init()
        self.display = Display(pg.image.load('assets/background.jpg'))
        self.player = None
        self.entities = []
        self.create_entities()
        self.clock = pg.time.Clock()
        self.running = True
        self.NEW_GHOST = pg.USEREVENT
        self.NEW_PUMPKIN = pg.USEREVENT + 1
        self.NEW_HEART = pg.USEREVENT + 2
        pg.time.set_timer(self.NEW_GHOST, 5000)
        pg.time.set_timer(self.NEW_PUMPKIN, 3000)
        pg.time.set_timer(self.NEW_HEART, 10000)
        self.difficulty = Difficulty.EASY
        self.kills_count = 0
        self.player_movement = None
        self.font = pg.font.Font('assets/Montserrat-Medium.ttf', 30)

    def create_entities(self):
        self.entities = [
            Ghost((rnd.randint(-200, 0), rnd.randint(0, self.display.HEIGHT // 4))),
            Pumpkin((rnd.randint(0, WIDTH), -100))
        ]
        self.player = Player((self.display.WIDTH / 2, self.display.HEIGHT - 200), 'player_stand')

    def check_collision(self):
        for e in self.entities:
            if not e.check_collision(self.player):
                continue
            if isinstance(e, Ghost):
                self.player.damage(1)
            if isinstance(e, Pumpkin):
                self.player.damage(10)
                self.entities.remove(e)
            if isinstance(e, Heart):
                self.player.heal(20)
                self.entities.remove(e)

    def run_events(self):
        for event in pg.event.get():
            if event.type == self.NEW_GHOST:
                self.create_new_enemies_wave(Ghost)
            if event.type == self.NEW_PUMPKIN:
                self.create_new_enemies_wave(Pumpkin)
            if event.type == self.NEW_HEART:
                self.drop_heart()
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONUP:
                clicked_enemy = self.get_enemy_under_cursor(pg.mouse.get_pos())
                if clicked_enemy is not None:
                    self.process_damage(clicked_enemy, 1)
            if event.type == pg.KEYUP:
                self.player.sprite = self.player.sprites['player_stand']

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.player_movement = ((1, 0), 5)
        if keys[pg.K_LEFT]:
            self.player_movement = ((-1, 0), 5)

    def drop_heart(self):
        x = rnd.randint(0, WIDTH - 100)
        self.entities.append(Heart((x, -100)))

    def update(self):
        if self.player_movement is not None:
            self.player.update(offset=self.player_movement, sprite=self.player.sprites['player_run'])
            self.player_movement = None
        for entity in self.entities:
            if isinstance(entity, Ghost):
                entity.update(dest=(self.player.rect.center, 2))
            if isinstance(entity, Pumpkin):
                entity.update(offset=((0, 1), 7))
                if entity.rect.centery >= HEIGHT - 100:
                    self.entities.remove(entity)
            if isinstance(entity, Heart):
                entity.update(offset=((0, 1), 2))

    def create_new_enemies_wave(self, enemy):
        if enemy is Ghost:
            for i in range(rnd.randint(1, self.difficulty.value[0])):
                pos = (-100 if rnd.randint(0, 100) % 2 == 0 else WIDTH + 100, rnd.randint(0, HEIGHT))
                self.entities.append(Ghost(pos))
        if enemy is Pumpkin:
            pos = (self.player.rect.centerx, -50)
            self.entities.append(Pumpkin(pos))

    def get_enemy_under_cursor(self, pos):
        for e in self.entities:
            if e.rect.collidepoint(pos):
                return e

    def process_damage(self, enemy, damage):
        enemy.damage(damage)
        if not enemy.alive:
            self.kills_count += 1
            self.entities.remove(enemy)

    def game_over(self):
        pg.display.set_caption('Game Over')
        self.running = True
        self.create_entities()
        self.run()

    def next_level(self):
        if self.difficulty == Difficulty.EASY:
            self.difficulty = Difficulty.MEDIUM
        elif self.difficulty == Difficulty.MEDIUM:
            self.difficulty = Difficulty.HARD
        elif self.difficulty == Difficulty.HARD:
            self.difficulty = Difficulty.UNREAL

    def run(self):
        while self.running:
            self.run_events()
            if self.kills_count >= self.difficulty.value[1]:
                self.next_level()
            self.update()
            self.check_collision()

            text = self.font.render(f'Kills: {self.kills_count}', True, WHITE)
            self.display.draw(text, (20, 20), self.player, *self.entities)

            pg.display.set_caption(f'Level {self.difficulty.name} | FPS: {self.clock.get_fps()}')
            if not self.player.alive:
                self.running = False

            self.clock.tick(FPS)
        self.game_over()
