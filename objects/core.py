import pygame

from settings import TILE_SIZE


class Object(object):
    offset = (0, 0)
    width = 0
    length = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_collision_box(self):
        if self.width == 0 or self.length == 0:
            return None

    def draw(self, screen, chunk_x, chunk_y, camera_x, camera_y):
        screen.blit(self.get_image(), (
            chunk_x * TILE_SIZE + self.x - camera_x - self.offset[0],
            chunk_y * TILE_SIZE + self.y - camera_y - self.offset[1]
        ))


