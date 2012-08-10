import pygame, math, sys
from pygame.locals import *
pygame.init()
screen= pygame.display.set_mode((1024, 768))
BLACK = (0,0,0)
BLUE = (135, 199, 218)
screen.fill(BLUE)
BLACK = (0,0,0)
clock = pygame.time.Clock()

while True:
    #clock.tick(30)
    screen.fill(BLUE)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue 
        if event.type == KEYDOWN:
            if event.key == K_UP: print "Up key"
            elif event.key == K_DOWN: print "Down Key"
            elif event.key == K_ESCAPE: sys.exit(0)

