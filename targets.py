import pygame, sys, os, display, missiles, random, groups
from pygame.locals import *

class Oldlady(pygame.sprite.Sprite):
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("oldlady.png", -1)
        self.r_image = self.image 
        self.l_image = pygame.transform.flip(self.image, True, False)
        self.rect.left = ip
        self.rect.top = (display.env.floor - self.rect.height)
        self.next_update_time = 0
        self.going_right = True
        self.step = random.randrange(2, 15, 1)
                
    def update(self, current_time):
        if self.next_update_time <= current_time:
            if self.going_right: self.rect.left += self.step
            else: self.rect.left -= self.step
                
            if self.rect.left <= 0: 
                self.going_right = True                     #starts walking other way
                self.image = self.r_image
#                self.image, trash = display.load_image("oldladyright.png", -1)
            
            if self.rect.right >= display.env.right: #if she reaches the edge of the screen
                self.going_right = False
                self.image = self.l_image                            #starts walking other way
#                self.image, trash = display.load_image("oldladyleft.png", -1)
                #change image to reverse
            #move our position up or down by ten pixels
            
            self.next_update_time = current_time + 10

    def die(self):
        groups.targs.remove(self)
        
class Guard(pygame.sprite.Sprite):
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("gang1.png", -1)
        self.r_image = self.image
        self.l_image = pygame.transform.flip(self.image, True, False)
        self.rect.left = ip
        self.rect.top = (display.env.floor - self.rect.height)
        self.next_update_time = 0
        self.going_right = True
        self.step = random.randrange(2, 15, 1)
        self.next_shot = pygame.time.get_ticks() + display.env.fire_delay
        
    def update(self, current_time):
        if self.next_update_time <= current_time:
            if self.going_right: self.rect.left += self.step
            else: self.rect.left -= self.step
                
            if self.rect.left <= 0: 
                self.going_right = True                     #starts walking other way
                self.image = self.r_image
            
            if self.rect.right >= display.env.right:   #if she reaches the edge of the screen
                self.going_right = False        #starts walking other way
                self.image = self.l_image
                #change image to reverse
                
            #move our position up or down by ten pixels
            self.next_update_time = current_time + 10
        
        if current_time > self.next_shot:
            self.shoot()
            self.next_shot = current_time + display.env.fire_delay
            
    def shoot(self):
        if self.going_right: groups.eshots.add(missiles.Bullets(self.rect.topright, (5, -5)))
        if self.going_right == False: groups.eshots.add(missiles.Bullets(self.rect.topleft, (-5, -5)))
        
    def die(self):
        groups.targs.remove(self)

rand = random.randrange
       
for x in range(3):
    groups.targs.add(Guard(rand(1, (display.env.right))))       #starts Guards random loc
    groups.targs.add(Oldlady(rand(1, (display.env.right))))     #starts OldLady random loc
