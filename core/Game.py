from shutil import copyfile

import pygame

from SaveManager import SaveManager
from core.scene.SceneManager import SceneManager


class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False

        self.save_manager = SaveManager()
        self.scene_manager = SceneManager(self.screen, self)
        self.active_save = None

    def run(self):
        while not self.done:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.done = True

            pressed = pygame.key.get_pressed()
            scene = self.scene_manager.get_current_scene()
            scene.process_input(pressed, events)
            scene.render()

            pygame.display.flip()
            self.clock.tick(60)

    def end(self):
        self.done = True
