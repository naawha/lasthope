from tinydb import TinyDB, Query

from Character import Character


class SaveGame(object):
    def __init__(self, savefile, loaded=True):
        self.savefile = savefile
        self.character = self.load_character()
        self.name, self.seed = self.get_data()

    def get_player_data(self):
        table = self.savefile.table('player')
        player = table.all()[0]
        player.pop('character')
        return player

    def get_data(self):
        table = self.savefile.table('game')
        data = table.all()[0]
        return data['name'], data['seed']

    def load_character(self):
        table = self.savefile.table('player')
        player = table.all()[0]
        return Character(**player['character'])

    def insert_objects(self, object_list):
        table = self.savefile.table('objects')
        table.insert_multiple(object_list)

    def has_chunk(self, x, y):
        table = self.savefile.table('chunks')
        q = Query()
        return bool(table.search((q.x == x) & (q.y == y)))

    def get_chunk_objects(self, x, y):
        table = self.savefile.table('objects')
        q = Query()
        return table.search((q.chunk_x == x) & (q.chunk_y == y))

    def insert_chunk(self, x, y):
        table = self.savefile.table('chunks')
        table.insert({
            'x': x,
            'y': y
        })
