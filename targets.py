import pygame, sys, os, display, missiles, random, groups
from pygame.locals import *

class Oldlady(pygame.sprite.Sprite):
    def __init__(self, ip, map_xpos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("oldlady.png", -1)
        self.r_image = self.image 
        self.l_image = pygame.transform.flip(self.image, True, False)
        self.range = display.env.scale *2
        self.rect.top = (display.env.floor - self.rect.height)
        self.next_update_time = 0
        self.going_right = False
        self.step = random.randrange(2, display.env.windspeed, 1)
        self.rect.left = ip - map_xpos
        self.relative_xpos = ip
        self.limit_l, self.limit_r = self.relative_xpos - self.range, self.relative_xpos+ self.range/2
        self.value = 1000
                
    def update(self, current_time, map_xpos):

        if self.next_update_time <= current_time:
            if self.going_right:
                self.relative_xpos += self.step*2
            else: self.relative_xpos -= self.step
            
            if self.relative_xpos <= self.limit_l: 
                self.going_right = True                     #starts walking other way
                self.image = self.r_image
            
            if self.relative_xpos + self.rect.width >= self.limit_r: #if she reaches the edge of the screen
                self.going_right = False
                self.image = self.l_image                            #starts walking other way
                #change image to reverse
            
            self.rect.left = self.relative_xpos - map_xpos
            
            self.next_update_time = current_time + 10

    def die(self):
        groups.targs.remove(self)
        
class Guard(pygame.sprite.Sprite):
    def __init__(self, ip, map_xpos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("gang1.png", -1)
        self.r_image = self.image 
        self.l_image = pygame.transform.flip(self.image, True, False)
        self.range = display.env.scale *2
        self.rect.top = (display.env.floor - self.rect.height)
        self.next_update_time = 0
        self.going_right = False
        self.step = random.randrange(2, 15, 1)
        self.rect.left = ip - map_xpos
        self.relative_xpos = ip
        self.limit_l, self.limit_r = self.relative_xpos - self.range, self.relative_xpos+ self.range/2
        self.next_shot = pygame.time.get_ticks() + display.env.fire_delay
        self.value = 1000

        
    def update(self, current_time, map_xpos):
        if self.next_update_time <= current_time:
            if self.going_right:
                self.relative_xpos += self.step *2
            else: self.relative_xpos -= self.step
            
            if self.relative_xpos <= self.limit_l: 
                self.going_right = True                     #starts walking other way
                self.image = self.r_image
            
            if self.relative_xpos + self.rect.width >= self.limit_r: #if she reaches the edge of the screen
                self.going_right = False
                self.image = self.l_image                            #starts walking other way
                #change image to reverse
            
            self.rect.left = self.relative_xpos - map_xpos
        
        if current_time > self.next_shot:
            self.shoot()
            self.next_shot = current_time + display.env.fire_delay
            
    def shoot(self):
        if self.going_right: groups.eshots.add(missiles.Bullets(self.rect.topright, (5, -5)))
        if self.going_right == False: groups.eshots.add(missiles.Bullets(self.rect.topleft, (-5, -5)))
        
    def die(self):
        groups.targs.remove(self)

rand = random.randrange
