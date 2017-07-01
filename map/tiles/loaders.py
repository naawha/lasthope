from core import spritesheet
from settings import TILE_SIZE


class TileLoader(object):
    SPRITE_KEYS = {
        'single_small': 0,
        'single_big': 3,

        'inner_top_left': 1,
        'inner_top_right': 2,
        'inner_bottom_left': 4,
        'inner_bottom_right': 5,

        'outer_top_left': 6,
        'outer_top_middle': 7,
        'outer_top_right': 8,
        'outer_middle_left': 9,
        'plain': 10,
        'outer_middle_right': 11,
        'outer_bottom_left': 12,
        'outer_bottom_middle': 13,
        'outer_bottom_right': 14,

        'plain_special_1': 15,
        'plain_special_2': 16,
        'plain_special_3': 17,

    }

    def __init__(self, key):
        self.spritesheet = self.get_spritesheet(key)

    def get_spritesheet(self, key):
        if key == 'grass':
            file = 'src/tiles/grass1.png'
        elif key == 'sand':
            file = 'src/tiles/sand1.png'
        elif key == 'water':
            file = 'src/tiles/water.png'
        elif key == 'sandwater':
            file = 'src/tiles/sandwater.png'
        else:
            raise Exception(u'Unknown key')
        return spritesheet.sprite_sheet((TILE_SIZE, TILE_SIZE), file)

    def get_sprite(self, key):
        return self.spritesheet[self.SPRITE_KEYS[key]]


GrassTileLoader = TileLoader('grass')
SandTileLoader = TileLoader('sand')
SandWaterTileLoader = TileLoader('sandwater')
WaterTileLoader = TileLoader('water')