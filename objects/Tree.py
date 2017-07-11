import pygame

from core import Object


treeImage = pygame.image.load('src/objects/tree1.png').convert_alpha()


class Tree(Object):
    offset = (44, 136)

    def get_image(self):
        return treeImage