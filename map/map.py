# -*- coding:utf-8 -*-
import random
from chunk import Chunk
from tinydb import TinyDB, Query
from settings import CHUNK_SIZE, TILE_SIZE
from tiles import GrassTile

CHUNK_PX_SIZE = CHUNK_SIZE * TILE_SIZE


class Map(object):
    def __init__(self, screen, savegame, x, y, seed):
        self.screen = screen
        self.savegame = savegame
        self.seed = seed
        self.chunk_x, self.chunk_y = self.get_chunk_coords(x, y)
        self.chunks = self.get_chunks()

    def get_chunk_coords(self, x, y):
        return int(x) / CHUNK_PX_SIZE, int(y) / CHUNK_PX_SIZE

    def get_chunks(self):
        chunks = []
        for y in range(self.chunk_y-1, self.chunk_y+2):
            for x in range(self.chunk_x-1, self.chunk_x+2):
                if hasattr(self, 'chunks'):
                    for chunk in self.chunks:
                        if chunk.x == x and chunk.y == y:
                            chunks.append(chunk)
                            break
                    else:
                        chunks.append(self.load_chunk(x, y))
                else:
                    chunks.append(self.load_chunk(x, y))
        return chunks

    def load_chunk(self, x, y):
        if self.savegame.has_chunk(x, y):
            objects = self.savegame.get_chunk_objects(x, y)
        else:
            self.savegame.insert_chunk(x, y)
            objects = self.generate_objects(x, y)
            self.savegame.insert_objects(objects)
        return Chunk(x, y, self.seed, objects)

    def generate_objects(self, x, y):
        temp_chunk = Chunk(x, y, self.seed, [])
        trees = []
        trees_count = 20
        for i in range(trees_count):
            obj_x = random.randint(0, CHUNK_PX_SIZE)
            obj_y = random.randint(0, CHUNK_PX_SIZE)
            try:
                if isinstance(temp_chunk.map[(obj_y/32)*CHUNK_SIZE+obj_x/32], GrassTile):
                    trees.append({
                        'type': 'tree',
                        'chunk_x': x,
                        'chunk_y': y,
                        'x': obj_x,
                        'y': obj_y
                    })
            except:
                pass

        return trees

    def update(self, x, y):
        chunk_x, chunk_y = self.get_chunk_coords(x, y)
        if chunk_x != self.chunk_x or chunk_y != self.chunk_y:
            self.chunk_x = chunk_x
            self.chunk_y = chunk_y
            self.chunks = self.get_chunks()

    def render(self, camera_x, camera_y, player):
        for i in range(len(self.chunks)):
            self.chunks[i].render_tiles(self.screen, camera_x, camera_y)

        for i in range(len(self.chunks)):
            if i == 4:
                self.chunks[i].render_objects(self.screen, camera_x, camera_y, player)
            else:
                self.chunks[i].render_objects(self.screen, camera_x, camera_y)

    def filter_movement_new(self, movement, player_x, player_y, camera_x, camera_y):
        filtered_movement = [movement[0], movement[1]]
        water_dive = 0
        _new_player = [player_x-camera_x+movement[0], player_y-camera_y+movement[1]]
        box = self.get_collision_box((player_x, player_y))

        if not box[1].is_walkable and box[1].rect.collidepoint(*_new_player):
            filtered_movement[1] = movement[1] - (_new_player[1] - box[1].rect.bottom - 1)

        if not box[7].is_walkable and box[7].rect.collidepoint(*_new_player):
            filtered_movement[1] = movement[1] - (_new_player[1] - box[7].rect.top + 1)

        if not box[3].is_walkable and box[3].rect.collidepoint(*_new_player):
            filtered_movement[0] = movement[0] - (_new_player[0] - box[3].rect.right - 1)

        if not box[5].is_walkable and box[5].rect.collidepoint(*_new_player):
            filtered_movement[0] = movement[0] - (_new_player[0] - box[5].rect.left + 1)

        return filtered_movement, water_dive

    def box_collision(self, box, player):
        if box[1] > player[0] > box[3] and box[0] < player[1] < box[2]:
            return True
        return False

    def filter_obj_movement(self, movement, player_x, player_y, camera_x, camera_y):
        filtered_movement = [movement[0], movement[1]]
        _new_player = [player_x+movement[0], player_y+movement[1]]
        for obj in self.chunks[4].objects:
            box = obj.get_collision_box()
            if box is not None and self.box_collision(box, _new_player):
                return [0, 0]
        return filtered_movement

    def filter_movement(self, movement, player_x, player_y, camera_x, camera_y):
        filtered_movement = [0, 0]
        water_dive = 0

        current_chunk = self.chunks[4]
        player_chunk_x = player_x - current_chunk.x * CHUNK_PX_SIZE
        player_chunk_y = player_y - current_chunk.y * CHUNK_PX_SIZE

        tile_chunk_x = int(player_chunk_x/TILE_SIZE)*TILE_SIZE
        tile_chunk_y = int(player_chunk_y/TILE_SIZE)*TILE_SIZE

        # индексы тайла, на котором находится игрок, относительно чанка
        tile_chunk_index_x = int(player_chunk_x/TILE_SIZE)
        tile_chunk_index_y = int(player_chunk_y/TILE_SIZE)

        current_tile = current_chunk.map[tile_chunk_index_y*TILE_SIZE+tile_chunk_index_x]
        result_tile = current_tile
        movement = [x*current_tile.movespeed_multiplier for x in movement]

        movement_inside_tile = True
        gaps = [0, 0]

        if movement[0]:
            if movement[0] < 0:
                gap = player_chunk_x - tile_chunk_x
            else:
                gap = tile_chunk_x + TILE_SIZE - 1 - player_chunk_x

            gaps[0] = gap
            if abs(gap) < abs(movement[0]):
                movement_inside_tile = False

        if movement[1]:
            if movement[1] < 0:
                gap = player_chunk_y - tile_chunk_y
            else:
                gap = tile_chunk_y + TILE_SIZE - 1 - player_chunk_y

            gaps[1] = gap
            if abs(gap) < abs(movement[1]):
                movement_inside_tile = False

        if movement_inside_tile:
            filtered_movement = movement
        else:
            player = (player_x, player_y)
            filtered_movement, result_tile = self.check_collisions(player, movement, gaps)
            if result_tile is None:
                result_tile = current_tile

        if result_tile.tile_type == 'water':
            player_tile_x = (player_x + filtered_movement[0])%TILE_SIZE
            player_tile_y = (player_y + filtered_movement[1])%TILE_SIZE
            water_dive = result_tile.get_dive((player_tile_x, player_tile_y))

        return filtered_movement, water_dive

    def get_corner_tile(self, collision_box, movement):
        collision_tile = None
        if movement[0] < 0 and movement[1] < 0:
            collision_tile = collision_box[0]
        if movement[0] > 0 and movement[1] < 0:
            collision_tile = collision_box[2]
        if movement[0] > 0 and movement[1] > 0:
            collision_tile = collision_box[8]
        if movement[0] < 0 and movement[1] > 0:
            collision_tile = collision_box[6]
        return collision_tile

    def get_y_tile(self, collision_box, movement):
        collision_tile = None
        if movement[1] < 0:
            collision_tile = collision_box[1]
        if movement[1] > 0:
            collision_tile = collision_box[7]

        if collision_tile is None:
            class DummyTile(object):
                def __init__(self):
                    self.is_walkable = False
            return DummyTile()
        return collision_tile

    def get_x_tile(self, collision_box, movement):
        collision_tile = None
        if movement[0] < 0:
            collision_tile = collision_box[3]
        if movement[0] > 0:
            collision_tile = collision_box[5]

        if collision_tile is None:
            class DummyTile(object):
                def __init__(self):
                    self.is_walkable = False
            return DummyTile()
        return collision_tile

    def check_collisions(self, player, movement, gaps):
        result_tile = None
        result_movement = [0, 0]
        collision_box = self.get_collision_box(player)

        only_one_movement = bool(movement[0]) != bool(movement[1])
        two_movements = not only_one_movement
        only_x_movement = only_one_movement and movement[0]
        only_y_movement = only_one_movement and movement[1]
        x_collides = abs(movement[0]) > abs(gaps[0])
        y_collides = abs(movement[1]) > abs(gaps[1])
        only_one_collides = x_collides != y_collides
        only_x_collides = x_collides and only_one_collides
        only_y_collides = y_collides and only_one_collides
        two_collisions = x_collides and y_collides
        x_walkable = self.get_x_tile(collision_box, movement).is_walkable
        y_walkable = self.get_y_tile(collision_box, movement).is_walkable

        if two_movements and two_collisions and self.get_corner_tile(collision_box, movement).is_walkable:
            result_movement = movement
            result_tile = self.get_corner_tile(collision_box, movement)

        elif only_x_movement or only_x_collides or two_collisions and x_walkable and (not y_walkable or gaps[0] >= gaps[1]):
            if two_movements and only_x_collides:
                result_movement[1] = movement[1]
            if self.get_x_tile(collision_box, movement).is_walkable:
                result_movement[0] = movement[0]
                result_tile = self.get_x_tile(collision_box, movement)
            else:
                result_movement[0] = gaps[0]

        elif only_y_movement or only_y_collides or two_collisions and y_walkable and (not x_walkable or gaps[0] < gaps[1]):
            if two_movements and only_y_collides:
                result_movement[0] = movement[0]
            if self.get_y_tile(collision_box, movement).is_walkable:
                result_movement[1] = movement[1]
                result_tile = self.get_y_tile(collision_box, movement)
            else:
                result_movement[1] = gaps[1]

        return result_movement, result_tile

    def get_tile(self, chunk, x, y):
        return chunk.map[y*CHUNK_SIZE+x]

    def get_relative_tile(self, player_x, player_y, relative_x, relative_y):
        current_chunk = self.chunks[4]

        # координаты игрока относительно текущего чанка
        player_chunk_x = player_x - current_chunk.x * CHUNK_PX_SIZE
        player_chunk_y = player_y - current_chunk.y * CHUNK_PX_SIZE

        # индексы тайла, на котором находится игрок, относительно чанка
        tile_chunk_index_x = int(player_chunk_x/TILE_SIZE)
        tile_chunk_index_y = int(player_chunk_y/TILE_SIZE)

        # сырые координаты
        raw_x = tile_chunk_index_x + relative_x
        raw_y = tile_chunk_index_y + relative_y

        # подсчёт реальных координам нужного тайла
        if raw_x < 0:
            coord_x = CHUNK_SIZE - 1
        elif raw_x >= CHUNK_SIZE:
            coord_x = CHUNK_SIZE - raw_x
        else:
            coord_x = raw_x

        if raw_y < 0:
            coord_y = CHUNK_SIZE - 1
        elif raw_y >= CHUNK_SIZE:
            coord_y = CHUNK_SIZE - raw_y
        else:
            coord_y = raw_y

        # определение чанка, в котором находится нужный тайл
        chunk = None
        x_lt = raw_x < 0
        x_in = 0 <= raw_x < CHUNK_SIZE
        x_gt = raw_x >= CHUNK_SIZE

        y_lt = raw_y < 0
        y_in = 0 <= raw_y < CHUNK_SIZE
        y_gt = raw_y >= CHUNK_SIZE

        if x_lt and y_lt:
            chunk = self.chunks[0]
        elif x_in and y_lt:
            chunk = self.chunks[1]
        elif x_gt and y_lt:
            chunk = self.chunks[2]
        elif x_lt and y_in:
            chunk = self.chunks[3]
        elif x_in and y_in:
            chunk = self.chunks[4]
        elif x_gt and y_in:
            chunk = self.chunks[5]
        elif x_lt and y_gt:
            chunk = self.chunks[6]
        elif x_in and y_gt:
            chunk = self.chunks[7]
        elif x_gt and y_gt:
            chunk = self.chunks[8]

        if not chunk:
            return None
        return self.get_tile(chunk, coord_x, coord_y)

    def get_collision_box(self, player):
        return [
            self.get_relative_tile(player[0], player[1], -1, -1),
            self.get_relative_tile(player[0], player[1], 0, -1),
            self.get_relative_tile(player[0], player[1], 1, -1),
            self.get_relative_tile(player[0], player[1], -1, 0),
            self.get_relative_tile(player[0], player[1], 0, 0),
            self.get_relative_tile(player[0], player[1], 1, 0),
            self.get_relative_tile(player[0], player[1], -1, 1),
            self.get_relative_tile(player[0], player[1], 0, 1),
            self.get_relative_tile(player[0], player[1], 1, 1),
        ]
