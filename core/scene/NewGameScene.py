import pygame

from AbstractScene import AbstractScene
from mixins import SubMenuMixin
from core.interface import NewGameInterface


class NewGameScene(SubMenuMixin, AbstractScene):
    def get_interface(self):
        return NewGameInterface(self.screen, self.manager)
