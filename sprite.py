import pygame as pg


def load_sprites():
    sprites = {}
    for sprite in Sprite.sprite_table.items():
        name, data = sprite
        sprites[name] = Sprite(data)
    return sprites


class Sprite:
    sprite_table = {
        'player_stand':
            {
                'path': 'assets/sprites/player_sprite.png',
                'width': 37,
                'height': 57,
                'speed': 5,
                'scale': 3,
                'coords': [(39, 21), (78, 21), (116, 21), (153, 21), (191, 21), (231, 21)],
            },
        'player_run':
            {
                'path': 'assets/sprites/player_sprite.png',
                'width': 39,
                'height': 57,
                'speed': 4,
                'scale': 3,
                'coords': [(282, 21), (319, 21), (355, 21), (392, 21), (433, 21), (470, 21), (510, 21), (550, 21)],
            },
        'ghost_fly':
            {
                'path': 'assets/sprites/ghost_sprite.png',
                'width': 31,
                'height': 46,
                'speed': 5,
                'scale': 3,
                'coords': [(0, 0), (32, 0), (64, 0), (96, 0)],
            },
        'pumpkin':
            {
                'path': 'assets/sprites/pumpkin/1.png',
                'width': 64,
                'height': 64,
                'speed': 1,
                'scale': 1,
                'coords': [(0, 0)]
            },
        'heart':
            {
                'path': 'assets/sprites/heart.png',
                'width': 64,
                'height': 64,
                'speed': 1,
                'scale': 0.7,
                'coords': [(0, 0)]
            }
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
        self.__flipped = False

    def get_sprite_from_image(self, sprite_coords):
        x, y = sprite_coords
        frame = self.sprite_sheet.subsurface(x, y, self.width, self.height)
        frame = pg.transform.scale(frame, (int(self.width * self.scale), int(self.height * self.scale)))
        if self.__flipped:
            frame = pg.transform.flip(frame, self.__flipped, False)
        return frame

    def get_current_frame(self):
        self.frames_counter += 1
        if self.frames_counter > self.speed:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprite_coords)
            self.frames_counter = 0
        return self.get_sprite_from_image(self.sprite_coords[self.sprite_index])

    def flip(self, flag):
        self.__flipped = flag
