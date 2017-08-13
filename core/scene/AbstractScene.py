class AbstractScene(object):
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.interface = self.get_interface()

    def process_input(self, pressed, events):
        pass

    def get_interface(self):
        return None

    def render(self):
        self.screen.fill((0, 0, 0))
        self.interface.render()
