# -*- coding: utf=8 -*-
import pygame
from settings import MENU_TYPES
from core.spritesheet import sprite_sheet


class Menu(object):
    OFFSET_TOP = 0
    OFFSET_LEFT = 0
    menu_type = 'big'
    default = 0
    item_height = 1
    items = []
    return_on_select = True

    def select_item(self, i):
        raise NotImplementedError

    def __init__(self, screen):
        self.settings = MENU_TYPES[self.menu_type]
        self.screen = screen
        self.images = self.get_images()
        self.active = self.default
        self.move_ticker = 0
        self.clickable = [None for x in self.items]

    def process_event(self, event):
        max_item_index = len(self.items) - 1
        if event.type == pygame.KEYDOWN:
            if len(self.items) > 1:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.active is None:
                        self.active = max_item_index
                    else:
                        self.active = self.active - 1 if self.active > 0 else max_item_index
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.active is None:
                        self.active = 0
                    else:
                        self.active = self.active + 1 if self.active < max_item_index else 0
            if event.key == pygame.K_RETURN:
                if self.return_on_select:
                    return self.items[self.active]['key']
                else:
                    self.select_item(self.active)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in range(len(self.clickable)):
                rect = self.clickable[i]
                if rect.collidepoint(x, y):
                    self.active = i
                    if self.return_on_select:
                        return self.items[i]['key']
                    else:
                      self.select_item(i)

    def get_images(self):
        return sprite_sheet((self.settings[0], self.settings[1]), self.settings[2])

    def render_item(self, i, active, left, top):
        pass

    def render(self):
        top = self.OFFSET_TOP
        self.screen.blit(self.images[0], (self.OFFSET_LEFT, top))
        top += self.settings[1]
        for i in xrange(len(self.items)):
            item_top = top
            active = (i == self.active)
            for j in xrange(self.item_height):
                self.screen.blit(self.images[1], (self.OFFSET_LEFT, top))
                top += self.settings[1]
            self.render_item(i, active, self.OFFSET_LEFT, item_top)
            self.clickable[i] = pygame.Rect(self.OFFSET_LEFT, item_top, self.settings[0],
                                            self.settings[1]*self.item_height)
        self.screen.blit(self.images[2], (self.OFFSET_LEFT, top))