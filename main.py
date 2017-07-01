import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from core.game import Game
game = Game(screen)
game.run()
