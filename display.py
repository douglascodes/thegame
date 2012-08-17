import pygame, sys, os, main, random
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
windspeed = 5
max_health = 300
rand = random.randrange

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

class Cloud(pygame.sprite.Sprite):                      #background clouds, A La mario bros
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        cloudtype = rand(1,5)
        self.image, self.rect = load_image("cloud{}.png".format(cloudtype), -1) #picks from 5 images
        self.speed = (windspeed - 2) + cloudtype                        #speed = windspeed + cloudtype
        self.rect.top = rand(-50, (_floor - self.rect.height - 10) )    
        self.rect.right = rand(-100, -10)
        self.next_update_time = 0
                
    def update(self, current_time):
        if self.next_update_time <= current_time:
            self.rect.left += self.speed
            self.next_update_time = current_time + 4
        
        if self.rect.left > _right: self.die()
        

    def die(self):
        main.cloud_grp.remove(self)