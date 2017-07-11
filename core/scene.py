# -*- coding:utf-8 -*-

import pygame
from tinydb import Query

from core.player import Player
from map import Map
from interface import MainMenu, PauseMenu, NewGameInterface, LoadGameInterface
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, CAMERA_OFFSET


class AbstractScene(object):
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.interface = self.get_interface()

    def process_input(self, pressed, events):
        pass

    def get_interface(self):
        return None

    def render(self):
        self.screen.fill((0, 0, 0))
        self.interface.render()


class SubMenuMixin(object):
    def process_input(self, pressed, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                self.interface.click(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.back_to_menu()


class MenuScene(AbstractScene):
    def __init__(self, screen, game):
        super(MenuScene, self).__init__(screen, game)
        self.menu = MainMenu(self.get_menu_items(), screen)

    def get_menu_items(self):
        items = [('newgame', u'Новая игра')]
        if self.has_savegames():
            items.append(('loadgame', u'Загрузить'))
        items.append(('settings', u'Настройки'))
        items.append(('quit', u'Выход'))

        return items

    def has_savegames(self):
        return bool(self.game.get_savegames())

    def apply_action(self, key):
        if key == 'newgame':
            self.game.show_new_game()
        if key == 'loadgame':
            self.game.show_load_game()
        if key == 'quit':
            self.game.end()

    def process_input(self, pressed, events):
        for event in events:
            selected = self.menu.process_event(event)
            if selected:
                self.apply_action(selected)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.menu.render()


class NewGameScene(SubMenuMixin, AbstractScene):
    def get_interface(self):
        return NewGameInterface(self.screen, self.game)


class LoadGameScene(SubMenuMixin, AbstractScene):
    def get_interface(self):
        return LoadGameInterface(self.screen, self.game)

    def process_input(self, pressed, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.back_to_menu()
            self.interface.process_event(event)


class MapScene(AbstractScene):
    def __init__(self, game, screen, player, map):
        super(MapScene, self).__init__(screen, game)
        self.player = player
        self.map = map
        self.game_menu = None

        self.x = self.y = None
        self.center_camera()

    def center_camera(self):
        self.x = self.player.x - SCREEN_WIDTH/2
        self.y = self.player.y - SCREEN_HEIGHT/2

    def open_menu(self):
        self.game_menu = PauseMenu([
            ('continue', u'Продолжить'),
            ('save', u'Сохранить'),
            ('settings', u'Настройки'),
            ('main_menu', u'В меню'),
            ('exit', u'Выйти')
        ], self.screen)

    def close_menu(self):
        self.game_menu = None

    @staticmethod
    def decide_move_direction(pressed):
        run = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]
        move_keys = {
            'top': pressed[pygame.K_w] or pressed[pygame.K_UP],
            'bottom': pressed[pygame.K_s] or pressed[pygame.K_DOWN],
            'left': pressed[pygame.K_a] or pressed[pygame.K_LEFT],
            'right': pressed[pygame.K_d] or pressed[pygame.K_RIGHT],
        }
        if move_keys['top'] and move_keys['bottom']:
            move_keys['top'] = move_keys['bottom'] = False
        if move_keys['left'] and move_keys['right']:
            move_keys['left'] = move_keys['right'] = False
        direction = [key for key, value in move_keys.items() if value]
        return direction, run

    def pause_menu_event(self, event):
        if event == 'continue':
            self.close_menu()
        if event == 'save':
            self.game.save_game()
            self.close_menu()
        if event == 'settings':
            self.close_menu()
        if event == 'main_menu':
            self.game.back_to_menu()
        if event == 'exit':
            self.game.end()

    def process_input(self, pressed, events):
        if self.game_menu:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.close_menu()
                    return
                selected = self.game_menu.process_event(event)
                if selected:
                    self.pause_menu_event(selected)
        else:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.open_menu()
                    return
            direction, run = self.decide_move_direction(pressed)
            self.move_player(direction, run)

    def move_player(self, direction, run):
        if not direction:
            self.player.idle = True
            self.player.run = False
            return

        self.player.direction = direction
        movement = self.player.get_movement(direction, run)
        movement, water_dive = self.map.filter_movement(movement, self.player.x, self.player.y)

        camera_movement = [0, 0]

        player_screen_position_x = self.player.x - self.x
        player_screen_position_y = self.player.y - self.y

        if movement[0] or movement[1]:
            if movement[0]:
                if movement[0] > 0:
                    screen_offset_gap = SCREEN_WIDTH - player_screen_position_x - CAMERA_OFFSET
                    if screen_offset_gap < movement[0]:
                        camera_movement[0] = movement[0] - screen_offset_gap
                elif movement[0] < 0:
                    screen_offset_gap = player_screen_position_x - CAMERA_OFFSET
                    if screen_offset_gap < -movement[0]:
                        camera_movement[0] = -(movement[0] - screen_offset_gap)
            if movement[1]:
                if movement[1] > 0:
                    screen_offset_gap = SCREEN_HEIGHT - player_screen_position_y - CAMERA_OFFSET
                    if screen_offset_gap < movement[1]:
                        camera_movement[1] = movement[1] - screen_offset_gap
                elif movement[1] < 0:
                    screen_offset_gap = player_screen_position_y - CAMERA_OFFSET
                    if screen_offset_gap < -movement[1]:
                        camera_movement[1] = -(movement[1] - screen_offset_gap)

            # print camera_movement
            self.player.apply_movement(movement, run, water_dive)
            self.apply_movement(camera_movement)

    def apply_movement(self, movement):
        self.x += movement[0]
        self.y += movement[1]

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map.update(self.player.x, self.player.y)
        self.map.render(self.x, self.y, self.player)

        if self.game_menu:
            self.game_menu.render()
