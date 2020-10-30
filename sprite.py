import pygame as pg
from constants import *


class Sprite:

    sprite_table = {
        'player_static_stand':
            {
                'path': 'assets/sprites/player_sprite.png',
                'width': 37,
                'height': 57,
                'speed': 5,
                'scale': 5,
                'coords': [(39, 21), (78, 21), (116, 21), (153, 21), (191, 21), (231, 21)],
            },
        'ghost_fly':
            {
                'path': 'assets/sprites/ghost_sprite.png',
                'width': 31,
                'height': 46,
                'speed': 5,
                'scale': 5,
                'coords': [(0, 0), (32, 0), (64, 0), (96, 0)],
            },
    }

    def __init__(self, sprite_info):
        self.sprite_sheet = pg.image.load(sprite_info['path'])
        self.sprite_sheet.convert_alpha()
        self.width = sprite_info['width']
        self.height = sprite_info['height']
        self.sprite_coords = sprite_info['coords']
        self.speed = sprite_info['speed']
        self.scale = sprite_info['scale']
        self.sprite_index = 0
        self.frames_counter = 0

    def get_sprite_from_image(self, sprite_coords):
        x, y = sprite_coords
        frame = self.sprite_sheet.subsurface(x, y, self.width, self.height)
        return pg.transform.scale(frame, (self.width * self.scale, self.height * self.scale))

    def get_current_frame(self):
        self.frames_counter += 1
        if self.frames_counter > self.speed:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprite_coords)
            self.frames_counter = 0
        return self.get_sprite_from_image(self.sprite_coords[self.sprite_index])


