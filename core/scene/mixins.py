import pygame


class SubMenuMixin(object):
    interface = None
    manager = None

    def process_input(self, pressed, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                self.interface.click(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.back_to_menu()
