import pygame, sys, os, display, main, random
from pygame.locals import *

class Oldlady(pygame.sprite.Sprite):
    def __init__(self, ip):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("oldladyright.png")
        self.rect.left = ip
        self.rect.top = (display._floor - self.rect.height)
        self.next_update_time = 0
        self.going_right = True
        self.step = random.randrange(2, 15, 1)
                
    def update(self, current_time):
        if self.next_update_time <= current_time:
            if self.going_right: self.rect.left += self.step
            else: self.rect.left -= self.step
                
            if self.rect.left <= 0: 
                self.going_right = True                     #starts walking other way
                self.image, trash = display.load_image("oldladyright.png")
            
            if self.rect.right >= display._right: #if she reaches the edge of the screen
                self.going_right = False                            #starts walking other way
                self.image, trash = display.load_image("oldladyleft.png")
                #change image to reverse
                
            #move our position up or down by ten pixels
            
            self.next_update_time = current_time + 10

    def die(self):
        pass