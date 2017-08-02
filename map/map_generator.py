import random

from opensimplex import OpenSimplex
from PIL import Image, ImageDraw

from settings import CHUNK_SIZE
from tiles import SandTile, WaterTile, GrassTile

def get_color(value):
    if value < 25:
        return (0, 21, 255)
    elif value < 35:
        return (255, 234, 0)
    elif value < 70:
        return (0, 171, 34)
    else:
        return (8, 120, 8)


def get_tile(value):
    if value < 25:
        return 'deepwater'
    if value < 30:
        return 'water'
    elif value < 35:
        return 'sand'
    else:
        return 'grass'


def make_img(x, y, array):
    img = Image.new("RGB", (CHUNK_SIZE, CHUNK_SIZE))
    draw = ImageDraw.Draw(img)
    i = j = 0
    for j in xrange(CHUNK_SIZE):
        for i in xrange(CHUNK_SIZE):
            color = get_color(array[j][i])
            draw.point((j, i), color)
    img.save("test%s%s.png" % (x, y), "PNG")


def noise(gen, nx, ny):
    return gen.noise2d(nx, ny) / 2.0 + 0.5


def generate_chunk_2(seed, chunk_x, chunk_y):
    gen = OpenSimplex(seed)
    chunk = []
    # img = []
    for y in range(chunk_y*CHUNK_SIZE, (chunk_y+1)*CHUNK_SIZE):
        # row = []
        for x in range(chunk_x*CHUNK_SIZE, (chunk_x+1)*CHUNK_SIZE):
            nx = x*1.0/CHUNK_SIZE - 0.5
            ny = y*1.0/CHUNK_SIZE - 0.5
            # e = (
            #     1.0 * noise(gen, 1*nx, 1*ny) +
            #     1.0 * noise(gen, 2*nx, 2*ny)
            # )
            # e /= (1.00 + 1.00)
            e = 0.5 * noise(gen, 1*nx, 1*ny)
            e /= 0.5
            e = pow(e, 1.5)
            e = int(round(e, 2)*100)
            # row.append(e)
            chunk.append(get_tile(e))
        # img.append(row)
    # make_img(chunk_x, chunk_y, img)
    return chunk

