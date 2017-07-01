from settings import SAND_WATER
from tile import Tile
from loaders import WaterTileLoader
from loaders import SandTileLoader


class DeepWaterTile(Tile):
    is_walkable = False
    movespeed_multiplier = 0.5
    tile_type = 'deepwater'

    def get_image(self):
        return WaterTileLoader.get_sprite('plain_special_1')
