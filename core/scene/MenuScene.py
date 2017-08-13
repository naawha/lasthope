# -*- coding:utf-8 -*-
from AbstractScene import AbstractScene
from core.interface import MainMenu


class MenuScene(AbstractScene):
    def __init__(self, screen, manager):
        super(MenuScene, self).__init__(screen, manager)
        self.menu = MainMenu(self.get_menu_items(), screen)

    def get_menu_items(self):
        items = [('newgame', u'Новая игра')]
        print self.manager.has_savegames()
        if self.manager.has_savegames():
            items.append(('loadgame', u'Загрузить'))
        items.append(('settings', u'Настройки'))
        items.append(('quit', u'Выход'))
        return items

    def apply_action(self, key):
        if key == 'newgame':
            self.manager.show_new_game()
        if key == 'loadgame':
            self.manager.show_load_game()
        if key == 'quit':
            self.manager.end()

    def process_input(self, pressed, events):
        for event in events:
            selected = self.menu.process_event(event)
            if selected:
                self.apply_action(selected)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.menu.render()
