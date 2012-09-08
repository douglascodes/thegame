import pygame, sys, os, random, groups
from pygame.locals import *

rand = random.randrange

class Env():
    def __init__(self): 
        self.scale = 256
        self.bottom = self.scale * 3
        self.right = self.scale * 4
        self.BLUE = (135, 199, 218)
        self.BLACK = (0,0,0)
        self.initial_position = [100, 100]
        self.floor = self.bottom - 64
        self.windspeed = 5
        self.max_health = 300
        self.step = 20
        self.screen = pygame.display.set_mode((self.right, self.bottom))
        self.looptime = 30
        self.fire_delay = 1000
        
        pygame.init()
        pygame.display.flip()   
        pygame.key.set_repeat(1, self.looptime)
        
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

class Scenery(pygame.sprite.Sprite):         #Creates a ground/walkway for the floor
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)     
        self.get_graphic()
        self.image = self.graphic
        self.w = self.rect.width                             
        self.set_move_rate()
        self.set_tile_start()
        self.rect.top = self.start_tile_h
        self.rect.left = 0

    def get_graphic(self):
        self.graphic, self.rect = load_image("brick1.png", -1)

    def set_tile_start(self):
        self.start_tile_h = env.floor
        
    def set_move_rate(self):
        self.move_rate = 2
        
    def update(self, moving):                           #The ground will move at half the windspeed
        if moving:
                self.rect.left -= (env.windspeed / self.move_rate)     #Although maybe this will change
        if self.rect.left < -(env.windspeed + self.w):  #If ground goes to far left
            self.rect.left = -env.windspeed             #Set it to the left side (0) of the screen - windspeed 
        for x in range((env.right / self.w) + 2 ):     
            env.screen.blit(self.image, (x*self.w + self.rect.left, self.start_tile_h))
        #Finds the number of tiles needed, and adds 2. To keep the smoothness
        #Then draws the tiles over the foreground bottom.

class Ground(Scenery):         #Creates a ground/walkway for the floor
    def get_graphic(self):
        self.graphic, self.rect = load_image("brick1.png", -1)

class Hill(Scenery):         #Creates hil;ly background
    def get_graphic(self):
        self.graphic, self.rect = load_image("hills.png", -1) #picks the graphic

    def set_move_rate(self):
        self.move_rate = 3

    def set_tile_start(self):
        self.start_tile_h = env.floor - self.rect.height

class Cloud(pygame.sprite.Sprite):                      #background clouds, A La mario bros
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        cloudtype = rand(0,5)+1                           #Random number of clouds
        self.image, self.rect = load_image("cloud{}.png".format(cloudtype), -1) #picks from 5 images
        self.speed = (env.windspeed - 2) + cloudtype                        #speed = windspeed + cloudtype
        self.rect.top = rand(-10, (env.floor - self.rect.height - 100) )    #sets vertical range 
        self.rect.left = env.right + rand(1, env.scale*5)                               
        self.next_update_time = 0
        #A couple things going on here. Picks randomly from 5 cloud types, each with its own image
        #And relative speed based on the windspeed. Starts them a random distance off to the left side.
        #To keep them from clumping up too much. It needs some work.
                
    def update(self, current_time):                         #moves the cloud
        if self.next_update_time <= current_time:           #checks if it is time to update
            self.rect.left -= self.speed                    #moves it by the SPEED (based loosely on Wind)
            self.next_update_time = current_time + 7        #delays the next update
        #Since it depends on two variables windspeed and the update time
        #only one needs to change to make a difference in the apparent speed. Perhaps raising this
        #will put less pressure on the CPU though. Don't know
        
        if self.rect.right < 0: self.die()              #Off screen to right, kill it

    def die(self):
        groups.clouds.remove(self)             #dies by being removed from list.

env = Env()
g = Ground()                    #Creates the ground object known as G
h = Hill()
groups.road.add(g)              #Adds g to group for ground
groups.road.add(h)              #adds hill to group for background