from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT


class Tile(object):
    tile_type = None
    acceptable_tile_types = []

    def get_image(self):
        raise NotImplementedError

    def __init__(self, render_box):
        self.render_box = render_box
        self.image = self.get_image()
        self.rect = None

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
        tile_relative_x = chunk_x * TILE_SIZE + x * TILE_SIZE - camera_x
        tile_relative_y = chunk_y * TILE_SIZE + y * TILE_SIZE - camera_y
        if tile_relative_x + TILE_SIZE < 0 or tile_relative_y + TILE_SIZE < 0:
            return
        if tile_relative_x > SCREEN_WIDTH or tile_relative_y > SCREEN_HEIGHT:
            return

        new_rect = None
        image = self.image
        if type(image) is list:
            for i in image:
                new_rect = screen.blit(i, (
                    chunk_x * TILE_SIZE + x * TILE_SIZE - camera_x,
                    chunk_y * TILE_SIZE + y * TILE_SIZE - camera_y
                ))
        else:
            new_rect = screen.blit(image, (
                chunk_x * TILE_SIZE + x * TILE_SIZE - camera_x,
                chunk_y * TILE_SIZE + y * TILE_SIZE - camera_y
            ))
        self.rect = new_rect
