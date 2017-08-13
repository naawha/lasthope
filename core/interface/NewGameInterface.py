# -*- coding: utf=8 -*-
import pygame

from core.Character import Character
from core.spritesheet import sprite_sheet


class NewGameInterface(object):
    MARGIN_LEFT = 300
    MARGIN_TOP = 100
    PADDING_LEFT = 30
    PADDING_TOP = 64

    def __init__(self, screen, manager):
        self.direction = 'bottom'
        self.screen = screen
        self.manager = manager
        self.character = Character()
        self.images = self.get_images()

        self.font = pygame.font.Font('src/fonts/runic.ttf', 42)
        self.labels = self.get_labels()
        self.clickable = {}

        self._number_cache = {}

    def get_images(self):
        return {
            'scroll_giant': sprite_sheet((384, 64), 'src/menu/scroll_giant_right.png'),
            'sex': sprite_sheet((32, 32), 'src/menu/genderScrolls.png'),
            'panels': sprite_sheet((96, 96), 'src/menu/panels.png'),
            'scroll_big': sprite_sheet((192, 64), 'src/menu/big.png'),
            'arrows': sprite_sheet((20, 54), 'src/menu/arrows.png'),
            'buttons': sprite_sheet((96, 32), 'src/menu/buttons_horizontal.png'),
        }

    def get_number(self, number):
        if not number in self._number_cache:
            self._number_cache[number] = self.font.render(str(number), 1, (0, 0, 0))
        return self._number_cache[number]

    def get_labels(self):
        return {
            'skin': self.font.render(u'Цвет кожи', 1, (0, 0, 0)),
            'hair_style': self.font.render(u'Прическа', 1, (0, 0, 0)),
            'hair_color': self.font.render(u'Цвет волос', 1, (0, 0, 0)),
        }

    def render_character(self):
        margin_top = 100
        margin_left = 220

        self.character.render(self.screen, (
            self.MARGIN_LEFT + margin_left + 50,
            self.MARGIN_TOP + margin_top + 50
        ), direction=self.direction)

        left_rect = self.screen.blit(self.images['arrows'][0],
                                (self.MARGIN_LEFT + margin_left, self.MARGIN_TOP + margin_top))
        self.clickable['character_left'] = {
            'rect': left_rect,
            'func': self.turn_character,
            'args': ['left']
        }

        right_rect = self.screen.blit(self.images['arrows'][1],
                                 (self.MARGIN_LEFT + margin_left + 80, self.MARGIN_TOP + margin_top))
        self.clickable['character_right'] = {
            'rect': right_rect,
            'func': self.turn_character,
            'args': ['right']
        }

        arrow_margin_top = 65
        arrow_margin_left = 18

        offset_left = self.MARGIN_LEFT + margin_left + arrow_margin_left
        offset_top = self.MARGIN_TOP + margin_top + arrow_margin_top
        male_coords = (offset_left, offset_top)
        female_coords = (offset_left + 35, offset_top)

        male_img = None
        female_img = None
        if self.character.sex == 'male':
            male_img = self.images['sex'][1]
            female_img = self.images['sex'][2]
        elif self.character.sex == 'female':
            male_img = self.images['sex'][0]
            female_img = self.images['sex'][3]

        male_rect = self.screen.blit(male_img, male_coords)
        female_rect = self.screen.blit(female_img, female_coords)

        self.clickable['male'] = {
            'rect': male_rect,
            'func': self.character.set_sex,
            'args': ['male']
        }
        self.clickable['female'] = {
            'rect': female_rect,
            'func': self.character.set_sex,
            'args': ['female']
        }

    def turn_character(self, direction):
        directions = ['bottom', 'right', 'top', 'left']
        index = directions.index(self.direction)
        if direction == 'right':
            if index+1 == len(directions):
                index = 0
            else:
                index += 1
        if direction == 'left':
            index = directions.index(self.direction)
            if index == 0:
                index = len(directions)-1
            else:
                index -= 1
        self.direction = directions[index]

    def click(self, x, y):
        for key, ev in self.clickable.items():
            rect = ev['rect']
            if rect.collidepoint(x, y):
                ev['func'](*ev['args'])

    def render_scroll(self, size=3):
        SCROLL_SPRITE_HEIGHT = 64
        self.screen.blit(self.images['scroll_giant'][0], (self.MARGIN_LEFT, self.MARGIN_TOP))
        for i in xrange(size):
            self.screen.blit(self.images['scroll_giant'][1], (self.MARGIN_LEFT, self.MARGIN_TOP+SCROLL_SPRITE_HEIGHT*(i+1)))
        self.screen.blit(self.images['scroll_giant'][2], (self.MARGIN_LEFT, self.MARGIN_TOP+SCROLL_SPRITE_HEIGHT*(size+1)))

    def go_next(self):
        self.manager.create_game(self.character)

    def render_continue_button(self):
        button = self.screen.blit(self.images['buttons'][0], (
            self.MARGIN_LEFT + 225,
            self.MARGIN_TOP + 385
        ))

        self.clickable['next'] = {
            'rect': button,
            'func': self.go_next,
            'args': []
        }

    def render_settings(self):
        menu_elements = ['skin', 'hair_style', 'hair_color']

        margin_left = 0
        margin_top = 10
        elem_height = 125
        arrows_margin_top = 40
        offset_left = self.MARGIN_LEFT + self.PADDING_LEFT + margin_left

        i = 0
        for el in menu_elements:
            offset_top = self.MARGIN_TOP + self.PADDING_TOP + margin_top + elem_height * i

            self.screen.blit(self.labels[el], (offset_left, offset_top))
            rect_left = self.screen.blit(self.images['arrows'][0], (offset_left, offset_top + arrows_margin_top))
            self.clickable['settings_%s_left' % el] = {
                'rect': rect_left,
                'func': self.character.change_index,
                'args': [el, -1]
            }

            rect_right = self.screen.blit(self.images['arrows'][1], (offset_left + 100, offset_top + arrows_margin_top))
            self.clickable['settings_%s_right' % el] = {
                'rect': rect_right,
                'func': self.character.change_index,
                'args': [el, 1]
            }

            self.screen.blit(self.get_number(self.character.get_index(el)+1), (
                offset_left + 50,
                offset_top + 45)
            )
            i += 1

    def render(self):
        self.render_scroll(size=6)
        self.render_character()
        self.render_settings()
        self.render_continue_button()
