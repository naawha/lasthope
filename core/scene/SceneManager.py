from . import MenuScene, NewGameScene, LoadGameScene, MapScene


class SceneManager(object):
    def __init__(self, screen, game):
        self.screen = screen
        self._game = game
        self.default_scene = MenuScene(self.screen, self)
        self.current_scene = None

    def get_current_scene(self):
        return self.current_scene or self.default_scene

    def show_new_game(self):
        self.current_scene = NewGameScene(self.screen, self)

    def show_load_game(self):
        self.current_scene = LoadGameScene(self.screen, self)

    def back_to_menu(self):
        self.current_scene = None

    def has_savegames(self):
        return self._game.save_manager.has_savegames()

    def get_savegames(self):
        return self._game.save_manager.list()

    def load_game(self, savegame):
        savegame = self._game.save_manager.load(savegame)
        self._game.active_save = savegame
        self.current_scene = MapScene(self, self.screen, savegame)

    def create_game(self, character):
        savegame = self._game.save_manager.create(character)
        self.load_game(savegame)

    def end(self):
        self._game.end()
