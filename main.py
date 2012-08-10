import pygame, sys, math, os
from pygame.locals import *

pygame.init()

scale = 256
_bottom = scale * 3
_right = scale * 4
step = 60
screen = pygame.display.set_mode((_right, _bottom))
fpsClock = pygame.time.Clock()
BLUE = (135, 199, 218)
BLACK = (0,0,0)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLUE)
clock = pygame.time.Clock()
initial_position = [100, 100]        
    

class Player(pygame.sprite.Sprite):
    image = None
        
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        if Player.image is None:
            Player.image, Player.rect = load_image("balloon.png")
        
        self.image, self.rect = Player.image, Player.rect
        
        self.rect.topleft = initial_position
        self.score = 0
        self.health = 100.0
        self.traveled = 0 
        self.points = 0

    def die(self):
        pass
    
    def win(self):
        self.score = self.traveled + self.points + g1.bonus 
    
    def fire(self):
        pass
    
    def check_health(self):
        if self.health <= 0.0:
            self.health = 0.0
            self.die()
        if self.health >= 100.0:
            self.health = 100.0
                        
    def adj_health(self, amount):
        self.health += amount
        self.check_health()
        
    def move_vert(self, amount):
        curr = self.rect.topleft
        save, curr = curr
        curr += amount
        if curr >= _bottom - self.rect.height:
            curr = _bottom - self.rect.height
        if curr <= 0:
            curr = 0
        self.rect.topleft = [save, curr]
        
        
    def move_horz(self, amount):
        curr = self.rect.topleft
        curr, save = curr
        curr += amount
        if curr >= _right - self.rect.width:
            curr = _right - self.rect.width
        if curr <= 0:
            curr = 0           
        self.rect.topleft = [curr, save]

                             
class Obstacle:
    pass

class AirObs (Obstacle):
    pass

class LandObs (Obstacle):
    pass

class Goal:
    x = 10
    y = 100
    bonus = 1,000,000
    pass

class Map:
    length = 1000
    pass

class Attack:
    pass

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def check_key():
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: sys.exit(0)
            elif event.key == K_UP: p1.move_vert(-step)
            elif event.key == K_DOWN: p1.move_vert(step)
            elif event.key == K_LEFT: p1.move_horz(-step)
            elif event.key == K_RIGHT: p1.move_horz(step)
    
    
pygame.display.flip()   
p1 = Player()
g1 = Goal()
allsprites = pygame.sprite.RenderPlain(p1)
while p1.health:
    check_key()
            
            
    #fpsClock.tick(30)   
    screen.blit(background, (0,0))
    screen.blit(p1.image, p1.rect)
    pygame.display.flip()
    
