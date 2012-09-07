import pygame, sys, os, display, groups
from pygame.locals import *

class Fire(pygame.sprite.Sprite):
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("redball.png", -1)
        self.rect.topleft = ip
        self.next_update_time = 0

    def update(self, current_time):
        if self.next_update_time <= current_time:
            self.rect.top += 5
            self.rect.left -= display.env.windspeed / 2
                        
            if self.rect.top >= display.env.floor - self.rect.height: #if bomb hits the ground explode into a splash
                self.die()
            #move our position up or down by ten pixels
            
            self.next_update_time = current_time + 10

    def die(self):
        groups.splashes.add(Splash(self.rect.topleft))
        groups.pshots.remove(self) 

class Splash(pygame.sprite.Sprite):
    existence = 1200
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = display.load_image("splashmod.png", -1)
        self.rect.topleft = ip
        self.next_update_time = 0
        self.create_time = pygame.time.get_ticks()
                               
    def update(self, time):
        if time > self.create_time + self.existence:
            self.die()

    def die(self):
        groups.splashes.remove(self)
        
class Bullets(pygame.sprite.Sprite):
    def __init__(self, ip, player_xy):
        pygame.sprite.Sprite.__init__(self)
        
        #calculate trajectory for X, Y of direction.
        step = -5
        opp = float(ip[1] - player_xy[1])
        adj = float(ip[0] - player_xy[0])
        tang = opp / adj
        
        bigstep = tang * step
        
        if adj > 0:
            direction = (step, bigstep)
        else:
            direction = (bigstep, step)

        self.dir = direction
        self.image, self.rect = display.load_image("bullet.png", -1)
        if self.dir[0] < 0:        
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.bottomleft = ip
        self.next_update_time = 0
        self.power = 20
                
    def update(self, current_time):
        if self.next_update_time <= current_time:
            self.rect.move_ip(self.dir) 
            self.next_update_time = current_time + 10
        
        if self.rect.bottom < 0:
            self.die()        

    def die(self):
        groups.eshots.remove(self)