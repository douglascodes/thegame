import pygame, sys, os, random, main
from pygame.locals import *

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

class Goal:
    x = 10
    y = 100
    bonus = 1,000,000
    pass

class Map:
    def __init__(self): 
        self.length = 10000
        return

class Ground(pygame.sprite.Sprite):         #Creates a ground/walkway for the floor
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)     
        self.image, self.rect = load_image("brick3.png", -1) #picks the graphic
        self.w = self.rect.width                             
        self.rect.topleft = (-self.w,main.floor)
        self.end = (main.right, main.bottom)
        for x in range(main.right/self.w):
            main.screen.blit(self.image, (x*self.w, main.floor))

    def update(self):                       #The ground will move at half the windspeed
        self.rect.left -= (main.windspeed/2)     #Although maybe this will change
        if self.rect.left < -(main.windspeed + self.w):  #If ground goes to far left
            self.rect.left = -main.windspeed             #Set it to the left side (0) of the screen - windspeed 
        for x in range((main.right/self.w) + 2 ):     
            main.screen.blit(self.image, (x*self.w + self.rect.left, main.floor))
        #Finds the number of tiles needed, and adds 2. To keep the smoothness
        #Then draws the tiles over the foreground bottom.

class Cloud(pygame.sprite.Sprite):                      #background clouds, A La mario bros
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self)
        cloudtype = rand(1,5)                           #Random number of clouds
        self.image, self.rect = load_image("cloud{}.png".format(cloudtype), -1) #picks from 5 images
        self.speed = (main.windspeed - 2) + cloudtype                        #speed = windspeed + cloudtype
        self.rect.top = rand(-50, (main.floor - self.rect.height - 10) )    #sets vertical range 
        self.rect.right = rand(-1000, -1)                               
        self.next_update_time = 0
        #A couple things going on here. Picks randomly from 5 cloud types, each with its own image
        #And relative speed based on the windspeed. Starts them a random distance off to the left side.
        #To keep them from clumping up too much. It needs some work.
                
    def update(self, current_time):                         #moves the cloud
        if self.next_update_time <= current_time:           #checks if it is time to update
            self.rect.left += self.speed                    #moves it by the SPEED (based loosely on Wind)
            self.next_update_time = current_time + 4        #delays the next update
        #Since it depends on two variables windspeed and the update time
        #only one needs to change to make a difference in the apparent speed. Perhaps raising this
        #will put less pressure on the CPU though. Don't know
        
        if self.rect.left > main.right: self.die()              #Off screen to right, kill it

    def die(self):
        main.cloud_grp.remove(self)             #dies by being removed from list.