# -*- coding:utf-8 -*-
from spritesheet import sprite_sheet
from settings import DEBUG, HAIR_STYLES, HAIR_COLORS, SKINS
import pyganim_patch

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

PLAYER_SRITE_OFFSET_X = 0
PLAYER_SRITE_OFFSET_Y = 5

SPRITE_TYPES = [
    ('cast', True, 7, 0),
    ('spear', True, 8, 0),
    ('walk', True, 9, 1),
    ('hit', True, 6, 0),
    ('bow', True, 13, 0),
    ('death', False, 6, 0)
]
SPRITE_DIRECTIONS = ['top', 'left', 'bottom', 'right']
SPRITESHEET_LENGTH = 13
ANIMATION_DELAY = 100
RUN_MULTIPLIER = 2.0


def refresh_sprites_after(func):
    def func_wrapper(self, *args):
        func(self, *args)
        self.refresh_sprites()
    return func_wrapper


class Character(object):
    def __init__(self, screen, sex='male', skin='light', hair_color='black', hair_style='messy1', dress=None):
        self.screen = screen
        self._sex = self.validate_sex(sex)
        self._skin = self.validate_skin(skin)
        self._hair_color = self.validate_hair_color(hair_color)
        self._hair_style = self.validate_hair_style(hair_style)
        self._dress = dress

        self.sprites = None
        self._images = None
        self._animations = None
        self.refresh_sprites()

    @staticmethod
    def validate_sex(sex):
        if sex in ['male', 'female']:
            return sex
        raise ValueError(u'Неверное значение пола')

    @staticmethod
    def validate_skin(skin):
        if skin:
            return skin
        raise ValueError(u'Неверное значение цвета кожи')

    @staticmethod
    def validate_hair_color(hair_color):
        if hair_color in HAIR_COLORS:
            return hair_color
        raise ValueError(u'Неверное значение цвета волос')

    @staticmethod
    def validate_hair_style(hair_style):
        if hair_style in HAIR_STYLES:
            return hair_style
        raise ValueError(u'Неверное значение типа волос')

    @property
    def sex(self):
        return self._sex

    @property
    def hair_color(self):
        return self._hair_color

    @property
    def hair_style(self):
        return self._hair_style

    @property
    def skin(self):
        return self._skin

    @refresh_sprites_after
    def set_sex(self, sex):
        self._sex = self.validate_sex(sex)

    @refresh_sprites_after
    def set_skin(self, skin):
        self._skin = self.validate_skin(skin)

    @refresh_sprites_after
    def set_hair_color(self, hair_color):
        self._hair_color = self.validate_hair_color(hair_color)

    @refresh_sprites_after
    def set_hair_style(self, hair_style):
        self._hair_style = self.validate_hair_style(hair_style)

    def refresh_sprites(self):
        self.sprites = self.get_sprites()
        self._images = self.get_images()
        self._animations = self.get_animations()

    def change_index(self, element, direction):
        def get_new_index(array, index, direction):
            if direction > 0:
               if index+1 == len(array):
                   return 0
               else:
                   return index+1
            if direction <= 0:
               if index == 0:
                   return len(array)-1
               else:
                   return index-1

        index = self.get_index(element)
        if element == 'skin':
            self.set_skin(SKINS[get_new_index(SKINS, index, direction)])
        elif element == 'hair_color':
            self.set_hair_color(HAIR_COLORS[get_new_index(HAIR_COLORS, index, direction)])
        elif element == 'hair_style':
            self.set_hair_style(HAIR_STYLES[get_new_index(HAIR_STYLES, index, direction)])

    def get_index(self, element):
        if element == 'skin':
            return SKINS.index(self.skin)
        elif element == 'hair_color':
            return HAIR_COLORS.index(self.hair_color)
        elif element == 'hair_style':
            return HAIR_STYLES.index(self.hair_style)
        return None

    def get_body_file(self):
        return 'body/%s/%s.png' % (self._sex, self._skin)

    def get_cloth_file(self):
        return 'torso/chain/tabard/jacket_%s.png' % self._sex

    def get_sprites(self):
        layers = []
        body = self.get_body_file()
        layers.append(sprite_sheet((PLAYER_WIDTH, PLAYER_HEIGHT), 'src/%s' % body))
        cloth = self.get_cloth_file()
        if cloth:
            layers.append(sprite_sheet((PLAYER_WIDTH, PLAYER_HEIGHT), 'src/%s' % cloth))
        hair = self.get_hair_file()
        if hair:
            layers.append(sprite_sheet((PLAYER_WIDTH, PLAYER_HEIGHT), 'src/%s' % hair))
        return layers

    def get_hair_file(self):
        if self._hair_style == 'none':
            return None
        return 'hair/%s/%s/%s.png' % (self._sex, self._hair_style, self._hair_color)

    def get_animations(self):
        layers = self.sprites
        animation_layers = []
        for sprites in layers:
            animations = {}

            for spite_type in SPRITE_TYPES:
                if spite_type[1]:
                    animations[spite_type[0]] = {direction: [] for direction in SPRITE_DIRECTIONS}
                else:
                    animations[spite_type[0]] = []

            normal_delay = ANIMATION_DELAY
            run_delay = ANIMATION_DELAY/RUN_MULTIPLIER

            i = 0
            for sprite_type in SPRITE_TYPES:
                if sprite_type[1]:
                    for direction in SPRITE_DIRECTIONS:
                        sprite_slice = sprites[i+sprite_type[3]:i+sprite_type[2]]
                        animations[sprite_type[0]][direction] = pyganim_patch.PygAnimation([(x, normal_delay) for x in sprite_slice])
                        animations[sprite_type[0]][direction].play()
                        i += SPRITESHEET_LENGTH
                else:
                    sprite_slice = sprites[i+sprite_type[3]:i+sprite_type[2]]
                    animations[sprite_type[0]] = pyganim_patch.PygAnimation([(x, normal_delay) for x in sprite_slice])
                    animations[sprite_type[0]].play()
                    i += SPRITESHEET_LENGTH

            animation_layers.append(animations)
        return animation_layers

    def get_images(self):
        layers = self.sprites
        image_layers = []
        for sprites in layers:
            images = {}

            i = 0
            for direction in SPRITE_DIRECTIONS:
                images[direction] = {}
                images[direction]['normal'] = sprites[i*SPRITESHEET_LENGTH]
                i += 1
            image_layers.append(images)
        return image_layers

    def render(self, coords, idle=True, direction='bottom', dive_offset=0):
        player_sprite_coords = [
            coords[0]-PLAYER_WIDTH/2+PLAYER_SRITE_OFFSET_X,
            coords[1]-PLAYER_HEIGHT+PLAYER_SRITE_OFFSET_Y+dive_offset
        ]
        if idle:
            for layer in self._images:
                self.screen.blit(layer[direction]['normal'], player_sprite_coords, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT-dive_offset))
        else:
            for layer in self._animations:
                layer['walk'][direction].blit(self.screen, player_sprite_coords, (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT-dive_offset))
