import random
import operator
import pygame

from tiles import GrassTile, SandTile, WaterTile, DeepWaterTile
from settings import DEBUG, CHUNK_SIZE, TILE_SIZE
from map_generator import generate_chunk_2
from objects import Tree


class Chunk(object):
    def __init__(self, x, y, seed, objects):
        self.x = x
        self.y = y
        self.seed = seed
        self.map = self.get_map()
        self.label = self.get_label()
        self.rect = self.get_absolute_rect()
        self.objects = self.prepare_objects(objects)

    def get_map(self):
        return self.prepare_chunk(self.generate())

    def get_absolute_rect(self):
        CHUNK_PX_SIZE = TILE_SIZE * CHUNK_SIZE

        top = self.y * CHUNK_PX_SIZE
        left = self.x * CHUNK_PX_SIZE
        right = (self.x + 1) * CHUNK_PX_SIZE
        bottom = (self.y + 1) * CHUNK_PX_SIZE
        return [
            [left, top],
            [right, top],
            [right, bottom],
            [left, bottom]
        ]

    def get_camera_rect(self, camera):
        return [[x[0] - camera[0], x[1] - camera[1]] for x in self.rect]

    def get_label(self):
        myfont = pygame.font.SysFont("monospace", 18)
        return myfont.render('(%s:%s)' % (self.x, self.y), 1, (0, 0, 0))

    def generate(self):
        return generate_chunk_2(self.seed, self.x, self.y)

    def prepare_chunk(self, generated):
        map = []
        for y in xrange(CHUNK_SIZE):
            for x in xrange(CHUNK_SIZE):
                box = self.get_tile_render_box(generated, x, y)
                Tile = self.get_tile_class(generated[y*CHUNK_SIZE+x])
                map.append(Tile(box))
        return map

    def prepare_objects(self, raw_objects):
        objects = []
        sorted_objects = sorted(raw_objects, key=operator.itemgetter('y', 'x'))

        for obj in sorted_objects:
            if obj['type'] == 'tree':
                objects.append(Tree(x=obj['x'], y=obj['y']))
        return objects

    def get_tile_class(self, tile_type):
        if tile_type == 'grass':
            return GrassTile
        elif tile_type == 'sand':
            return SandTile
        elif tile_type == 'water':
            return WaterTile
        elif tile_type == 'deepwater':
            return DeepWaterTile
        return None

    def get_tile_render_box(self, generated, tile_x, tile_y):
        def get_tile_type(x, y):
            return generated[y*CHUNK_SIZE+x]

        render_box = [None for x in range(9)]
        if tile_x > 0 and tile_y > 0:
            render_box[0] = get_tile_type(tile_x-1, tile_y-1)
        if tile_y > 0:
            render_box[1] = get_tile_type(tile_x, tile_y-1)
        if tile_x < CHUNK_SIZE-1 and tile_y > 0:
            render_box[2] = get_tile_type(tile_x+1, tile_y-1)

        if tile_x > 0:
            render_box[3] = get_tile_type(tile_x-1, tile_y)
        render_box[4] = get_tile_type(tile_x, tile_y)
        if tile_x < CHUNK_SIZE-1:
            render_box[5] = get_tile_type(tile_x+1, tile_y)

        if tile_x > 0 and tile_y < CHUNK_SIZE-1:
            render_box[6] = get_tile_type(tile_x-1, tile_y+1)
        if tile_y < CHUNK_SIZE-1:
            render_box[7] = get_tile_type(tile_x, tile_y+1)
        if tile_x < CHUNK_SIZE-1 and tile_y < CHUNK_SIZE-1:
            render_box[8] = get_tile_type(tile_x+1, tile_y+1)
        return render_box

    def render_tiles(self, screen, camera_x, camera_y):
        chunk_x = self.x * CHUNK_SIZE
        chunk_y = self.y * CHUNK_SIZE

        for y in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                self.map[y*CHUNK_SIZE+x].draw(screen, x, y, chunk_x, chunk_y, camera_x, camera_y)

        if DEBUG:
            chunk_rect = self.get_camera_rect((camera_x, camera_y))
            border_size = 2

            even_x = self.x % 2 == 0
            even_y = self.y % 2 == 0
            if even_x == even_y:
                border_color = 0x000000
            else:
                border_color = 0xff0000

            pygame.draw.line(screen, border_color,
                             (chunk_rect[0][0], chunk_rect[0][1]),
                             (chunk_rect[1][0], chunk_rect[1][1]),
                             border_size)
            pygame.draw.line(screen, border_color,
                             (chunk_rect[1][0]-border_size, chunk_rect[1][1]),
                             (chunk_rect[2][0]-border_size, chunk_rect[2][1]),
                             border_size)
            pygame.draw.line(screen, border_color,
                             (chunk_rect[2][0]-border_size, chunk_rect[2][1]),
                             (chunk_rect[3][0]-border_size, chunk_rect[3][1]),
                             border_size)
            pygame.draw.line(screen, border_color,
                             (chunk_rect[2][0], chunk_rect[2][1]-border_size),
                             (chunk_rect[3][0], chunk_rect[3][1]-border_size),
                             border_size)
            pygame.draw.line(screen, border_color,
                             (chunk_rect[3][0], chunk_rect[3][1]),
                             (chunk_rect[0][0], chunk_rect[0][1]),
                             border_size)
            screen.blit(self.label, (chunk_rect[0][0]+20, chunk_rect[0][1]+20))

    def render_objects(self, screen, camera_x, camera_y, player=None):
        chunk_x = self.x * CHUNK_SIZE
        chunk_y = self.y * CHUNK_SIZE

        player_rendered = player is None
        for i in xrange(len(self.objects)):
            if not player_rendered:
                if player.y <= self.objects[i].y:
                    player.draw(camera_x, camera_y)
                    player_rendered = True
            self.objects[i].draw(screen, chunk_x, chunk_y, camera_x, camera_y)
        if not player_rendered:
            player.draw(camera_x, camera_y)
