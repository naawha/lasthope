import pygame

from settings import TILE_SIZE, CHUNK_SIZE


class Object(object):
    offset = (0, 0)
    width = 0
    length = 0

    def __init__(self, x, y, chunk_x, chunk_y):
        self.x = x + chunk_x * TILE_SIZE * CHUNK_SIZE
        self.y = y + chunk_y * TILE_SIZE * CHUNK_SIZE

    def get_collision_box(self):
        if self.width == 0 or self.length == 0:
            return None
        else:
            return [
                self.y - self.length / 2,
                self.x + self.width / 2,
                self.y + self.length / 2,
                self.x - self.width / 2,
            ]

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.get_image(), (
            self.x - camera_x - self.offset[0],
            self.y - camera_y - self.offset[1]
        ))


