import pygame as pg
from constants import *


class Display:
    def __init__(self, background):
        self.RES = self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.screen = pg.display.set_mode(self.RES)
        self.bg = pg.transform.scale(background, self.RES)

    def draw(self, *args):
        self.screen.blit(self.bg, (0, 0))
        # self.screen.fill(BLACK)
        for arg in args:
            arg.draw(self.screen)
        pg.display.flip()
