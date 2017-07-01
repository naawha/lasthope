# -*- coding:utf-8 -*-
from tile import Tile
from loaders import SandTileLoader, SandWaterTileLoader, WaterTileLoader, GrassTileLoader


class SandTile(Tile):
    is_walkable = True
    movespeed_multiplier = 1
    tile_type = 'sand'

    def get_image(self):
        render_box = self.render_box

        # прямые линии
        if self.compare_matrix([2, 0, 2,
                                1, 1, 1,
                                2, 2, 2]) and render_box[1] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_bottom_middle')
            ]

        elif self.compare_matrix([2, 1, 2,
                                  2, 1, 0,
                                  2, 1, 2]) and render_box[5] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_middle_left')
            ]
        elif self.compare_matrix([2, 2, 2,
                                  1, 1, 1,
                                  2, 0, 2]) and render_box[7] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_top_middle')
            ]
        elif self.compare_matrix([2, 1, 2,
                                  0, 1, 2,
                                  2, 1, 2]) and render_box[3] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_middle_right')
            ]

        # внутренние углы
        elif self.compare_matrix([2, 0, 0,
                                  1, 1, 0,
                                  2, 1, 2]) and render_box[1] == 'grass' and render_box[5] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('inner_top_right')
            ]
        elif self.compare_matrix([2, 1, 2,
                                  1, 1, 0,
                                  2, 0, 0]) and render_box[5] == 'grass' and render_box[7] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('inner_bottom_right')
            ]
        elif self.compare_matrix([2, 1, 2,
                                  0, 1, 1,
                                  0, 0, 2]) and render_box[3] == 'grass' and render_box[7] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('inner_bottom_left')
            ]

        elif self.compare_matrix([0, 0, 2,
                                  0, 1, 1,
                                  2, 1, 2]) and render_box[3] == 'grass' and render_box[1] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('inner_top_left')
            ]

        # внешние углы
        elif self.compare_matrix([2, 1, 0,
                                  2, 1, 1,
                                  2, 2, 2]) and render_box[2] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_bottom_left')
            ]
        elif self.compare_matrix([2, 2, 2,
                                  2, 1, 1,
                                  2, 1, 0]) and render_box[8] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_top_left')
            ]
        elif self.compare_matrix([2, 2, 2,
                                  1, 1, 2,
                                  0, 1, 2]) and render_box[6] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_top_right')
            ]

        elif self.compare_matrix([0, 1, 2,
                                  1, 1, 2,
                                  2, 2, 2]) and render_box[0] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_bottom_right')
            ]

        # границы точек
        elif self.compare_matrix([0, 1, 0,
                                  1, 1, 1,
                                  2, 2, 2]) and render_box[0] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_bottom_middle')
            ]
        elif self.compare_matrix([2, 1, 0,
                                  2, 1, 1,
                                  2, 1, 0]) and render_box[2] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_middle_left')
            ]
        elif self.compare_matrix([2, 2, 2,
                                  1, 1, 1,
                                  0, 1, 0]) and render_box[8] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_top_middle')
            ]
        elif self.compare_matrix([0, 1, 2,
                                  1, 1, 2,
                                  0, 1, 2]) and render_box[6] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                GrassTileLoader.get_sprite('outer_top_middle')
            ]

        # точки
        elif self.compare_matrix([2, 2, 2,
                                  0, 1, 0,
                                  2, 2, 2]) and render_box[3] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                WaterTileLoader.get_sprite('single_big')
            ]
        elif self.compare_matrix([2, 0, 2,
                                  2, 1, 2,
                                  2, 0, 2]) and render_box[1] == 'grass':
            return [
                SandTileLoader.get_sprite('plain'),
                WaterTileLoader.get_sprite('single_big')
            ]

        return SandTileLoader.get_sprite('plain')