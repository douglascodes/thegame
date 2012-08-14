import pygame, sys, os
from pygame.locals import *

step = 30
pygame.init()
BLUE = (135, 199, 218)
BLACK = (0,0,0)
scale = 256
_bottom = scale * 3
_right = scale * 4
screen = pygame.display.set_mode((_right, _bottom))
BLUE = (135, 199, 218)
BLACK = (0,0,0)
initial_position = [100, 100]
_floor = _bottom - 64

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()