import pygame

from AbstractScene import AbstractScene
from mixins import SubMenuMixin
from core.interface import LoadGameInterface


class LoadGameScene(SubMenuMixin, AbstractScene):
    def get_interface(self):
        return LoadGameInterface(self.screen, self.manager)

    def process_input(self, pressed, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.back_to_menu()
            self.interface.process_event(event)