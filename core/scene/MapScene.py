# -*- coding:utf-8 -*-
import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH, CAMERA_OFFSET
from AbstractScene import AbstractScene
from core.interface import PauseMenu
from map import Map
from core.Player import Player


class MapScene(AbstractScene):
    def __init__(self, manager, screen, savegame):
        super(MapScene, self).__init__(screen, manager)
        self.savegame = savegame
        self.player = self.load_player()
        self.map = self.load_map()
        self.game_menu = None

        self.x = self.y = None
        self.center_camera()

    def load_player(self):
        player_data = self.savegame.player_data
        return Player(self.screen, self.savegame.character, **player_data)

    def load_map(self):
        return Map(self.screen, self.savegame, self.player.x, self.player.y, seed=self.savegame.seed)

    def center_camera(self):
        self.x = self.player.x - SCREEN_WIDTH/2
        self.y = self.player.y - SCREEN_HEIGHT/2

    def open_menu(self):
        self.game_menu = PauseMenu(self.screen)

    def close_menu(self):
        self.game_menu = None

    def pause_menu_event(self, event):
        if event == 'continue':
            self.close_menu()
        if event == 'save':
            self.manager.save_game()
            self.close_menu()
        if event == 'settings':
            self.close_menu()
        if event == 'main_menu':
            self.manager.back_to_menu()
        if event == 'exit':
            self.manager.end()

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
        movement = self.map.filter_obj_movement(movement, self.player.x, self.player.y, self.x, self.y)
        movement, water_dive = self.map.filter_movement(movement, self.player.x, self.player.y, self.x, self.y)

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
