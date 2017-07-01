from tile import Tile
from loaders import WaterTileLoader
from loaders import GrassTileLoader


class GrassTile(Tile):
    is_walkable = True
    movespeed_multiplier = 1
    tile_type = 'grass'

    @staticmethod
    def get_image():
        return GrassTileLoader.get_sprite('plain')
