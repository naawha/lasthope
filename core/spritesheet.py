import pygame, sys
from pygame.locals import *


def sprite_sheet(size, file, pos=(0,0)):

    len_sprt_x, len_sprt_y = size
    sprt_rect_x, sprt_rect_y = pos
    sheet = pygame.image.load(file).convert_alpha() #Load the sheet
    sheet_rect = sheet.get_rect()
    sprites = []
    for i in range(0, sheet_rect.height, size[1]):
        for i in range(0,sheet_rect.width, size[0]):
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y))
            sprite = sheet.subsurface(sheet.get_clip())
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    return sprites
