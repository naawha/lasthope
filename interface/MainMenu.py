# -*- coding: utf=8 -*-
import pygame

from utils import Menu


class MainMenu(Menu):
    OFFSET_TOP = 100
    OFFSET_LEFT = 100

    def __init__(self, items, screen):
        self.items = self.prepare_items(items)
        super(MainMenu, self).__init__(screen)

    def prepare_items(self, items):
        prepared_items = []

        # myfont = pygame.font.SysFont("monospace", 18)
        font = pygame.font.Font('src/fonts/runic.ttf', 56)
        normal_color = (0, 0, 0)
        active_color = (255, 0, 0)

        for i in items:
            prepared_items.append({
                'normal': font.render(i[1], 1, normal_color),
                'active': font.render(i[1], 1, active_color),
                'key': i[0]
            })
        return prepared_items

    def render_item(self, i, active, top, left):
        if active:
            self.screen.blit(self.items[i]['active'], (top+20, left+10))
        else:
            self.screen.blit(self.items[i]['normal'], (top+20, left+10))

