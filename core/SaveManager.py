import datetime
import random
import os
from shutil import copyfile
from tinydb import TinyDB, Query

from SaveGame import SaveGame


class SaveManager(object):
    @staticmethod
    def create(character):
        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        world_seed = random.randint(100000000, 9999999999)
        savefile = TinyDB('save/%s.sav' % current_datetime)
        table = savefile.table('player')
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
        table = savefile.table('game')
        table.insert({
            'seed': world_seed,
            'name': current_datetime
        })

        savegame = SaveGame(savefile)
        return savegame

    def load(self, savegame):
        copyfile('save/%s.sav' % savegame.name, 'save/.current.sav')
        savefile = TinyDB('save/.current.sav')
        savegame = SaveGame(savefile)
        return savegame

    def list(self):
        savegames = []
        files = [f for f in os.listdir('save') if os.path.isfile(os.path.join('save', f))
                 and f.endswith('.sav') and not f.startswith('.')]
        for f in files:
            savefile = TinyDB(os.path.join('save', f))
            savegames.append(SaveGame(savefile))
        return savegames

    def has_savegames(self):
        files = [f for f in os.listdir('save') if os.path.isfile(os.path.join('save', f))
                 and f.endswith('.sav') and not f.startswith('.')]
        return bool(files)


