from settings import TILE_SIZE


class Tile(object):
    tile_type = None
    acceptable_tile_types = []

    def __init__(self, render_box):
        self.render_box = render_box
        self.image = self.get_image()

    def compare_matrix(self, matrix):
        for i in xrange(len(matrix)):
            if matrix[i] == 1 and self.render_box[i] != self.tile_type and \
                            self.render_box[i] not in self.acceptable_tile_types and self.render_box[i] is not None:
                return False
            if matrix[i] == 0 and (self.render_box[i] == self.tile_type or self.render_box[i] is None
                                   or self.render_box[i] in self.acceptable_tile_types):
                return False
        return True

    def draw(self, screen, x, y, chunk_x, chunk_y, camera_x, camera_y):
        image = self.image
        if type(image) is list:
            for i in image:
                screen.blit(i, (
                    chunk_x * TILE_SIZE + x * TILE_SIZE - camera_x,
                    chunk_y * TILE_SIZE + y * TILE_SIZE - camera_y)
                            )
        else:
            screen.blit(image, (
                chunk_x * TILE_SIZE + x * TILE_SIZE - camera_x,
                chunk_y * TILE_SIZE + y * TILE_SIZE - camera_y)
            )
