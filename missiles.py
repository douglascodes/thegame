import pygame, sys, os, display, main
from pygame.locals import *

class Fire(pygame.sprite.Sprite):
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("redball.png", -1)
        self.rect.topleft = ip
        self.next_update_time = 0
        self.going_down = True
                
    def update(self, current_time):
        if self.next_update_time <= current_time:
            if self.going_down: self.rect.top += 5
            
            if self.rect.top >= main.floor - self.rect.height: #if bomb hits the ground explode into a splash
                self.going_down = False
                self.die()
            #move our position up or down by ten pixels
            
            self.next_update_time = current_time + 10

    def die(self):
        main.p1.pop_splash(self.rect.topleft)
        main.pshots_grp.remove(self) 

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
        main.p1.splashes_grp.remove(self)
        
class Bullets(pygame.sprite.Sprite):
    def __init__(self, ip, dir):
        pygame.sprite.Sprite.__init__(self)
        self.dir = dir
        self.image, self.rect = display.load_image("bullet.png", -1)
        if dir[0] < 0:        
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
        main.eshots_grp.remove(self) 
