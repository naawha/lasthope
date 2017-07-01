# -*- coding:utf-8 -*-
import math

from settings import SAND_WATER, TILE_SIZE
from tile import Tile
from loaders import WaterTileLoader, SandWaterTileLoader
from loaders import SandTileLoader


class WaterTile(Tile):
    is_walkable = True
    movespeed_multiplier = 0.5
    tile_type = 'water'
    acceptable_tile_types = ['deepwater']
    render_type = None

    def get_dive(self, player):
        delta = 0

        if self.render_type == 'flat_top':
            delta = player[1]
        if self.render_type == 'flat_right':
            delta = TILE_SIZE-player[0]
        if self.render_type == 'flat_bottom':
            delta = TILE_SIZE-player[1]
        if self.render_type == 'flat_left':
            delta = player[0]

        if self.render_type == 'outer_bottom_left':
            delta = math.sqrt(player[1]**2+(TILE_SIZE-player[0])**2)
            # delta = max(player[1], TILE_SIZE-player[0])
        if self.render_type == 'outer_top_left':
            delta = math.sqrt((TILE_SIZE-player[1])**2+(TILE_SIZE-player[0])**2)
            # delta = max(TILE_SIZE-player[1], TILE_SIZE-player[0])
        if self.render_type == 'outer_top_right':
            delta = math.sqrt((TILE_SIZE-player[1])**2+player[0]**2)
            # delta = max(TILE_SIZE-player[1], player[0])
        if self.render_type == 'outer_bottom_right':
            delta = math.sqrt(player[1]**2+player[0]**2)
            # delta = max(player[1], player[0])

        if self.render_type == 'inner_top_right':
            delta = min(player[1], TILE_SIZE-player[0])
        if self.render_type == 'inner_bottom_right':
            delta = min(TILE_SIZE-player[1], TILE_SIZE-player[0])
        if self.render_type == 'inner_bottom_left':
            delta = min(TILE_SIZE-player[1], player[0])
        if self.render_type == 'inner_top_left':
            delta = min(player[1], player[0])

        if self.compare_matrix([1, 1, 1,
                                1, 1, 1,
                                1, 1, 1]):
            return 1
        if delta and delta > TILE_SIZE/2:
            return min((delta-TILE_SIZE/2)/(TILE_SIZE/2), 1)
        else:
            return 0


    def get_image(self):
        render_box = self.render_box

        # прямые линии
        if self.compare_matrix([2, 0, 2,
                                1, 1, 1,
                                2, 2, 2]) and render_box[1] == 'sand':
            self.render_type = 'flat_top'
            return SandWaterTileLoader.get_sprite('outer_bottom_middle')
        elif self.compare_matrix([2, 1, 2,
                                  2, 1, 0,
                                  2, 1, 2]) and render_box[5] == 'sand':
            self.render_type = 'flat_right'
            return SandWaterTileLoader.get_sprite('outer_middle_left')
        elif self.compare_matrix([2, 2, 2,
                                  1, 1, 1,
                                  2, 0, 2]) and render_box[7] == 'sand':
            self.render_type = 'flat_bottom'
            return SandWaterTileLoader.get_sprite('outer_top_middle')
        elif self.compare_matrix([2, 1, 2,
                                  0, 1, 2,
                                  2, 1, 2]) and render_box[3] == 'sand':
            self.render_type = 'flat_left'
            return SandWaterTileLoader.get_sprite('outer_middle_right')

        # внутренние углы
        elif self.compare_matrix([2, 0, 0,
                                  1, 1, 0,
                                  2, 1, 2]) and render_box[1] == 'sand' and render_box[5] == 'sand':
            self.render_type = 'inner_top_right'
            return SandWaterTileLoader.get_sprite('inner_top_right')
        elif self.compare_matrix([2, 1, 2,
                                  1, 1, 0,
                                  2, 0, 0]) and render_box[5] == 'sand' and render_box[7] == 'sand':
            self.render_type = 'inner_bottom_right'
            return SandWaterTileLoader.get_sprite('inner_bottom_right')
        elif self.compare_matrix([2, 1, 2,
                                  0, 1, 1,
                                  0, 0, 2]) and render_box[3] == 'sand' and render_box[7] == 'sand':
            self.render_type = 'inner_bottom_left'
            return SandWaterTileLoader.get_sprite('inner_bottom_left')

        elif self.compare_matrix([0, 0, 2,
                                  0, 1, 1,
                                  2, 1, 2]) and render_box[3] == 'sand' and render_box[1] == 'sand':
            self.render_type = 'inner_top_left'
            return SandWaterTileLoader.get_sprite('inner_top_left')

        # внешние углы
        elif self.compare_matrix([1, 1, 0,
                                  2, 1, 1,
                                  2, 2, 1]) and render_box[2] == 'sand':
            self.render_type = 'outer_bottom_left'
            return SandWaterTileLoader.get_sprite('outer_bottom_left')
        elif self.compare_matrix([2, 1, 1,
                                  1, 1, 1,
                                  1, 1, 0]) and render_box[8] == 'sand':
            self.render_type = 'outer_top_left'
            return SandWaterTileLoader.get_sprite('outer_top_left')
        elif self.compare_matrix([1, 2, 2,
                                  1, 1, 2,
                                  0, 1, 1]) and render_box[6] == 'sand':
            self.render_type = 'outer_top_right'
            return SandWaterTileLoader.get_sprite('outer_top_right')

        elif self.compare_matrix([0, 1, 1,
                                  1, 1, 2,
                                  1, 2, 2]) and render_box[0] == 'sand':
            self.render_type = 'outer_bottom_right'
            return SandWaterTileLoader.get_sprite('outer_bottom_right')

        # границы точек
        elif self.compare_matrix([0, 1, 0,
                                  1, 1, 1,
                                  2, 2, 2]) and render_box[0] == 'sand':
            self.render_type = 'flat_top'
            return SandWaterTileLoader.get_sprite('outer_bottom_middle')
        elif self.compare_matrix([2, 1, 0,
                                  2, 1, 1,
                                  2, 1, 0]) and render_box[2] == 'sand':
            self.render_type = 'flat_right'
            return SandWaterTileLoader.get_sprite('outer_middle_left')
        elif self.compare_matrix([2, 2, 2,
                                  1, 1, 1,
                                  0, 1, 0]) and render_box[8] == 'sand':
            self.render_type = 'flat_bottom'
            return SandWaterTileLoader.get_sprite('outer_top_middle')
        elif self.compare_matrix([0, 1, 2,
                                  1, 1, 2,
                                  0, 1, 2]) and render_box[6] == 'sand':
            self.render_type = 'flat_left'
            return SandWaterTileLoader.get_sprite('outer_top_middle')

        # точки
        elif self.compare_matrix([2, 2, 2,
                                  0, 1, 0,
                                  2, 2, 2]) and render_box[3] == 'sand':
            self.render_type = 'single'
            return [
                SandTileLoader.get_sprite('plain'),
                WaterTileLoader.get_sprite('single_big')
            ]
        elif self.compare_matrix([2, 0, 2,
                                  2, 1, 2,
                                  2, 0, 2]) and render_box[1] == 'sand':
            self.render_type = 'single'
            return [
                SandTileLoader.get_sprite('plain'),
                WaterTileLoader.get_sprite('single_big')
            ]

        return WaterTileLoader.get_sprite('plain')
