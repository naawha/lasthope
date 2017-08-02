from spritesheet import sprite_sheet
import pyganim_patch
import pygame

from settings import DEBUG, HAIR_STYLES, HAIR_COLORS

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

PLAYER_MAX_DIVE = 16

PLAYER_SRITE_OFFSET_X = 0
PLAYER_SRITE_OFFSET_Y = 5

SPEED = 3
ANIMATION_DELAY = 100
RUN_MULTIPLIER = 2.0


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


CAMERA_OFFSET = 100


class Player(object):
    def __init__(self, screen, character, x, y):
        self.character = character
        self.x = x
        self.y = y
        self.screen = screen
        self.water_dive = 0

        self.idle = True
        self.run = False
        self.direction = 'bottom'

    def may_run(self):
        return True

    def get_movement(self, direction, run=False):
        movement = [0, 0]

        movespeed = SPEED
        if run and self.may_run():
            movespeed *= RUN_MULTIPLIER
        if len(self.direction) >= 2:
            movespeed /= 2.0

        if 'top' in direction:
            movement[1] = -movespeed
        if 'right' in direction:
            movement[0] = movespeed
        if 'bottom' in direction:
            movement[1] = movespeed
        if 'left' in direction:
            movement[0] = -movespeed
        return movement

    def apply_movement(self, movement, run, water_dive):
        self.x += movement[0]
        self.y += movement[1]
        self.idle = False
        self.run = run
        self.water_dive = water_dive

    def move(self, direction, run=False):
        if not direction:
            self.idle = True
            self.run = False
            return

        self.idle = False
        self.run = run
        self.direction = direction

        movespeed = SPEED
        if self.run:
            movespeed *= RUN_MULTIPLIER
        if len(self.direction) >= 2:
            movespeed /= 2.0

        if 'top' in direction:
            if self.y > CAMERA_OFFSET:
                self.y -= movespeed
        if 'right' in direction:
            if self.x < 1024-CAMERA_OFFSET:
                self.x += movespeed
        if 'bottom' in direction:
            if self.y < 768-CAMERA_OFFSET:
                self.y += movespeed
        if 'left' in direction:
            if self.x > CAMERA_OFFSET:
                self.x -= movespeed

    def get_image_direction(self):
        if 'left' in self.direction:
            return 'left'
        if 'right' in self.direction:
            return 'right'
        if 'top' in self.direction:
            return 'top'
        if 'bottom' in self.direction:
            return 'bottom'

    def draw(self, camera_x, camera_y):
        dive_offset = PLAYER_MAX_DIVE*self.water_dive

        direction = self.get_image_direction()
        # self.map.update(int(self.x), int(self.y))

        self.character.render((self.x - camera_x, self.y - camera_y), self.idle, direction, dive_offset)
        if DEBUG:
            myfont = pygame.font.SysFont("monospace", 15)
            label = myfont.render('(%s:%s)' % (self.x, self.y), 1, (0, 0, 0))
            self.screen.blit(label, (self.x, self.y))

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y,
            'character': {
                'skin': self.character.skin,
                'sex': self.character.sex,
                'hair_style': self.character.hair_style,
                'hair_color': self.character.hair_color,
            }
        }
