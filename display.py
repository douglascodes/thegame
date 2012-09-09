import pygame, sys, os, random, groups
from pygame.locals import *

rand = random.randrange

class Environment():                                    #holds environment variables
    def __init__(self): 
        self.scale = 256                        #basic unit of size for the game environment
        self.bottom = self.scale * 3            #sets a 4:3 aspect ration
        self.right = self.scale * 4
        self.BLUE = (135, 199, 218)             #A background fill color for the sky (RGB)
        self.BLACK = (0,0,0)                    #An alternate background RGB set for black
        self.initial_position = [100, 100]      #sets the player initial position
        self.floor = self.bottom - 64           #sets a road level 64 pixels up from the bottom of the screen
        self.windspeed = 5                      #A very important modifier, affects clouds, background movement
        self.max_health = 300                   #Default player health
        self.step = 20                          #Player movement step variable
        self.screen = pygame.display.set_mode((self.right, self.bottom))    #Defines the game screen
        self.looptime = 30                      #A pacing timer to 30 FPS
        self.fire_delay = 1000                  #Default limiter for enemey/player shots
        
        pygame.init()
        pygame.display.flip()   
        pygame.key.set_repeat(1, self.looptime) #allows for continuous key presses at looptime rate 
        
def load_image(name, colorkey=None):            #Code from pygame tutorial for basic image loading
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

class Scenery(pygame.sprite.Sprite):         #Generic scenary class
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)     
        self.get_graphic()                      #Loads the individual graphic from class/sub
        self.image = self.graphic               #Copys that into the main image for instance
        self.w = self.rect.width                #Just a shorter way to read width from the rect
        self.set_move_rate()                    #Sets the scenery move speed
        self.get_tile_start()                   #gets the top limit for tiling
        self.rect.top = self.start_tile_h       #Sets it
        self.rect.left = 0                      #Sets the left side of tiling (0 is leftmost side of screen)

    def get_graphic(self):                      #method for retrieving the image
        self.graphic, self.rect = load_image("brick1.png", -1) 

    def get_tile_start(self):                   #Sets the floor tile start height
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
        self.graphic, self.rect = load_image("brick1.png", -1) #Need a better graphic here

class Hill(Scenery):         #Creates hilly background
    def get_graphic(self):
        self.graphic, self.rect = load_image("hills.png", -1) #picks the graphic

    def set_move_rate(self):    #Hills in the background scroll slow than the foreground
        self.move_rate = 3

    def get_tile_start(self):                               #Sets the floor Hill start height
        self.start_tile_h = env.floor - self.rect.height    #sits above the road

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
        #And relative speed based on the windspeed. Starts them a random distance off to the right side.
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

env = Environment()
g = Ground()                    #Creates the ground object known as G
h = Hill()
groups.road.add(g)              #Adds g to group for ground
groups.road.add(h)              #adds hill to group for background