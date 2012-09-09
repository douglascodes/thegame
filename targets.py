import pygame, sys, os, display, missiles, random, groups
from pygame.locals import *

class Target(pygame.sprite.Sprite): #Generic target class
    def __init__(self, ip, map_xpos):
        pygame.sprite.Sprite.__init__(self)
        self.get_graphic()                              #calls the individual graphic function for subclasses
        self.r_image = self.image = self.graphic        #assigns this as the right image and main image 
        self.l_image = pygame.transform.flip(self.image, True, False)   #flips the image for reverse direction assignment
        self.range = display.env.scale *2               #Default range for a moving character about half a screen
        self.rect.top = (display.env.floor - self.rect.height)  #sets the graphic to draw it from height to floor
        self.next_update_time = 0                       #the update delay timer
        self.going_right = True                         #all things start heading right
        self.step = display.env.windspeed               #uses windspeed as a the speed of movement
        self.rect.left = ip - map_xpos                  #places their location relative to screen
        self.relative_xpos = ip                         #places their real map pos... passed from main
        self.next_shot = pygame.time.get_ticks() + display.env.fire_delay
        self.limit_l, self.limit_r = self.relative_xpos - self.range, self.relative_xpos+ self.range/2
        self.get_value()

    def shoot(self, current_time, player_xy):
        pass

    def update(self, current_time, map_xpos, player_xy):
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
            
            self.shoot(current_time, player_xy)                        
            self.next_update_time = current_time + 10

    def get_graphic(self):
        self.graphic, self.rect = display.load_image("bullseye.png", -1)

    def get_value(self):
        self.value = 100

    def die(self):
        groups.targs.remove(self)

class Oldlady(Target):
    def get_graphic(self):
        self.graphic, self.rect = display.load_image("oldlady.png", -1)

    def get_value(self):
        self.value = 800

class Guard(Target):

    def get_graphic(self):
        self.graphic, self.rect = display.load_image("gang1.png", -1)

    def get_value(self):
        self.value = 1000
            
    def shoot(self, current_time, player_xy):
        if current_time <= self.next_shot:
            return
        
        self.next_shot = current_time + (display.env.fire_delay * 2)

        if self.going_right: groups.eshots.add(missiles.Bullets(self.rect.topright, player_xy))
        if self.going_right == False: groups.eshots.add(missiles.Bullets(self.rect.topleft, player_xy))

class Goal(Target):

    def get_graphic(self):
        self.graphic, self.rect = display.load_image("popcornstand.png", -1)

    def get_value(self):
        self.bonus = 1,000,000
        self.value = 0

    def update(self, current_time, map_xpos, player_xy):
        if self.next_update_time <= current_time:
            self.rect.right = self.relative_xpos - map_xpos
        
            self.next_update_time = current_time + 10
    
    def die(self):
        pass
        
rand = random.randrange
