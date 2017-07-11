import pygame
import datetime
from random import randint
from os import listdir
from os.path import isfile, join
from tinydb import TinyDB, Query
from shutil import copyfile

from scene import MenuScene, MapScene, NewGameScene, LoadGameScene
from core.character import Character
from core.player import Player
from map import Map


class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.menu_scene = MenuScene(self.screen, self)
        self.scene = None

        self.save = None

    def show_new_game(self):
        self.scene = NewGameScene(self.screen, self)

    def show_load_game(self):
        self.scene = LoadGameScene(self.screen, self)

    def get_savegames(self):
        savegames = []
        files = [f for f in listdir('save') if isfile(join('save', f)) and f.endswith('.sav') and not f.startswith('.')]
        for f in files:
            try:
                db = TinyDB(join('save', f))
                character = self.load_character(db)
                savegames.append({
                    'character': character,
                    'file': f
                })
            except Exception:
                continue
        return savegames

    def create_game(self, character):
        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        save = TinyDB('save/%s.sav' % current_datetime)
        table = save.table('player')
        table.insert({
            'x': 0,
            'y': 0,
            'character': {
                'skin': character.skin,
                'sex': character.sex,
                'hair_style': character.hair_style,
                'hair_color': character.hair_color,
            }
        })
        table = save.table('game')
        table.insert({
            'seed': randint(100000000, 9999999999),
            'name': current_datetime
        })
        self.load_game(current_datetime)

    def save_game(self):
        if isinstance(self.scene, MapScene):
            player = self.scene.player
            self.save.purge_table('player')
            table = self.save.table('player')
            table.insert(player.serialize())
            table = self.save.table('game')
            copyfile('save/.current.sav', 'save/%s.sav' % table.all()[0]['name'])

    def load_character(self, save):
        table = save.table('player')
        player = table.all()[0]
        return Character(self.screen, **player.pop('character'))

    def load_player(self, save):
        table = save.table('player')
        player = table.all()[0]
        player.pop('character')
        player['character'] = self.load_character(save)
        return Player(self.screen, **player)

    def load_map(self, save, player):
        table = save.table('game')
        world = table.all()[0]
        world.pop('name')
        return Map(self.screen, self, player.x, player.y, **world)

    def load_game(self, savename):
        copyfile('save/%s.sav' % savename, 'save/.current.sav')
        save = TinyDB('save/.current.sav')
        self.save = save
        player = self.load_player(save)
        map = self.load_map(save, player)
        self.scene = MapScene(self, self.screen, player, map)

    def back_to_menu(self):
        self.scene = None

    def run(self):
        while not self.done:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.done = True

            pressed = pygame.key.get_pressed()
            scene = self.scene or self.menu_scene
            scene.process_input(pressed, events)
            scene.render()

            pygame.display.flip()
            self.clock.tick(60)

    def end(self):
        self.done = True
