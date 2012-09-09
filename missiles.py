import pygame, sys, os, display, groups
from pygame.locals import *

class Fire(pygame.sprite.Sprite):                   #This is the player shot
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = display.load_image("redball.png", -1)   
        #Just a simple red ballon graphic
        self.rect.topleft = ip              
        #Sets the balloon start position to the bottom center of the player graphic                                           
        self.next_update_time = 0           #Sets the update timer

    def update(self, current_time):         #Moves the balloon downward each update
        if self.next_update_time <= current_time:   
            self.rect.top += 5              #Y axis movement
            self.rect.left -= display.env.windspeed / 2 
            #X axis movement. Gets a little drift from the current windspeed
                        
            if self.rect.top >= display.env.floor - self.rect.height: 
            #if bomb hits the ground creates splash object and dies
                self.die()
            
            #move our position up or down by ten pixels
            self.next_update_time = current_time + 10

    def die(self):          #Pops the balloon and spawns a splash object
        groups.splashes.add(Splash(self.rect.topleft))  #Adds the splash to group
        groups.pshots.remove(self)                      #Removes the ballon from shots

class Splash(pygame.sprite.Sprite): #Simple water splash when ballons pop
    existence = 1200                #This is the countdown timer til splash dissipates
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = display.load_image("splashmod.png", -1) #Dorky graphic for splash
        self.rect.topleft = ip                                      #Replaces the ballon IP
        self.next_update_time = 0                                   
        self.create_time = pygame.time.get_ticks()  #Sets a creation time
                               
    def update(self, time):         #Checks to see if the splash has been around too long
        if time > self.create_time + self.existence:    #It's too old
            self.die()                                  #Kill it

    def die(self):
        groups.splashes.remove(self)            #Removes itself from the splash group
        
class Bullets(pygame.sprite.Sprite):
    def __init__(self, ip, player_xy):
        pygame.sprite.Sprite.__init__(self)
        
        #calculate trajectory for X, Y of direction.
        #This code is still wonky and needs some work. 
        step = -5
        opp = float(ip[1] - player_xy[1])   
        #Calculates Tangent. Needs opposite side of right triangle
        adj = float(ip[0] - player_xy[0])
        #And adjacent side Tangent = Opposite or Adjacent
        tang = opp / adj
        
        bigstep = tang * step #Modifies STEP to get a proportional x,y step each update 
        #a 45* angle will have an equal step and bigstep
        
        if adj > 0: 
            direction = (step, bigstep)
        else:
            direction = (bigstep, step)

        self.dir = direction            #Keeping this a seperate line for now 
        self.image, self.rect = display.load_image("bullet.png", -1) #Loads bullet graphic 
        if self.dir[0] < 0:                                          #Bullet is going other way
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.bottomleft = ip       # Starts at top of the Target graphic    
        self.next_update_time = 0       
        self.power = 20                 #How much power the bullet has to damage the player
                
    def update(self, current_time):
        if self.next_update_time <= current_time:
            self.rect.move_ip(self.dir) 
            self.next_update_time = current_time + 10
        
        if self.rect.bottom < 0:
            self.die()        

    def die(self):
        groups.eshots.remove(self)