import pygame

from core import Object


treeImage = pygame.image.load('src/objects/tree1.png').convert_alpha()


class Tree(Object):
    width = 36
    length = 14
    offset = (44, 136)

    def get_image(self):
        return treeImage