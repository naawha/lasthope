# -*- coding: utf=8 -*-
import pygame
import datetime

from utils import Menu


class LoadGameInterface(Menu):
    menu_type = 'giant_left'
    item_height = 2
    default = None
    return_on_select = False

    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.font = pygame.font.Font('src/fonts/runic.ttf', 40)
        self.items = self.get_savegames()
        super(LoadGameInterface, self).__init__(screen)

    def get_savegames(self):
        return self.manager.get_savegames()

    def get_label(self, value, color):
        if not hasattr(self, '_values_cache'):
            self._values_cache = {}

        colors = {
            'normal': (0, 0, 0),
            'active': (255, 0, 0),
        }
        key = '%s_%s' % (value, color)
        if key not in self._values_cache:
            self._values_cache[key] = self.font.render(value, 1, colors[color])
        return self._values_cache[key]

    def select_item(self, i):
        self.manager.load_game(self.items[i])

    def render_item(self, i, active, left, top):
        self.items[i].character.render(self.screen, (left+self.settings[0]-50, top+75))
        self.items[i].character.render(self.screen, (left+self.settings[0]-50, top+75))

        key = 'active' if active else 'normal'
        value = datetime.datetime.strptime(self.items[i].name, '%Y%m%d%H%M%S').strftime('%d-%m-%Y')

        self.screen.blit(self.get_label(u' Начало:'+value, key), (left+50, top+10))
        self.screen.blit(self.get_label(u'Сыграно:'+value, key), (left+50, top+60))
