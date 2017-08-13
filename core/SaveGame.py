from tinydb import TinyDB, Query

from Character import Character


class SaveGame(object):
    def __init__(self, savefile, loaded=True):
        self.savefile = savefile
        self.character = self._load_character()
        self.player_data = self._get_player_data()
        self.name, self.seed = self._get_data()
        self._chunks = self._load_chunks()
        self._objects = self._load_objects()

    def _load_objects(self):
        table = self.savefile.table('objects')
        return table.all()

    def _load_chunks(self):
        table = self.savefile.table('chunks')
        print table.all()
        return table.all()

    def _get_player_data(self):
        table = self.savefile.table('player')
        player = table.all()[0]
        player.pop('character')
        return player

    def _get_data(self):
        table = self.savefile.table('game')
        data = table.all()[0]
        return data['name'], data['seed']

    def _load_character(self):
        table = self.savefile.table('player')
        player = table.all()[0]
        return Character(**player['character'])

    def insert_objects(self, object_list):
        self._objects += object_list

    def has_chunk(self, x, y):
        return bool(filter(lambda c: c['x'] == x and c['y'] == y, self._chunks))

    def get_chunk_objects(self, x, y):
        return filter(lambda o: o['chunk_x'] == x and o['chunk_y'] == y, self._objects)

    def insert_chunk(self, x, y):
        self._chunks.append({
            'x': x,
            'y': y
        })
