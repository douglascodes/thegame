import pygame, sys, os, display, main, missiles
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    image = None
        
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        if Player.image is None:
            Player.image, Player.rect = display.load_image("balloon.png", -1)
        
        self.image, self.rect = Player.image, Player.rect
        
        self.rect.topleft = display.initial_position            #sets the balloon start at ip 
        self.score = 0                                  #points total over game
        self.health = 100.0                             #current health is 100
        self.traveled = 0                               #tracks game length
        self.points = 0                                 #points this round
        self.playershots_grp = pygame.sprite.Group()    #sprite group for bombs
        self.splashes_grp = pygame.sprite.Group()       #sprite group for splashes 

    def update(self):
        display.screen.blit(self.image, self.rect)
    
    def die(self):                                  #sets death animation and
                                                    #kills the game
        pass
    
    def win(self):                                  #tabulates the round points
        self.score = self.traveled + self.points
    
    def fire_weapon(self):                          #drops a balloon
        self.playershots_grp.add(missiles.Fire(self.rect.midbottom))

    def pop_splash(self, ip):                          #drops a balloon
        self.splashes_grp.add(missiles.Splash(ip))
       
    def check_health(self):                         #checks the players current health
        if self.health <= 0.0:
            self.health = 0.0
            self.die()                              #runs death if health is 0
        if self.health >= 100.0:
            self.health = 100.0                     #if health bonus exceeds 100, set to 100
                        
    def adj_health(self, amount):                   #checks the players current health
        self.health += amount
        self.check_health()
        
    def move_vert(self, amount):                    #move the ballon vertically
        curr = self.rect.topleft                    #gets the current location as [x,y]
        save, curr = curr                           #splits the x,y of topleft
        curr += amount                              #increments Y by AMOUNT
        if curr >= display._floor - self.rect.height:      #limits the movement to outside border
            curr = display._floor - self.rect.height
        if curr <= 0:
            curr = 0
        self.rect.topleft = [save, curr]            #reassigns the X,Y to rect.topleft
        
        
    def move_horz(self, amount):
        curr = self.rect.topleft                    #gets the current location as [x,y]
        curr, save = curr                           #splits the x,y of topleft
        curr += amount                              #increments the X by AMOUNT
        if curr >= display._right - self.rect.width:        #limits the movement to outside border
            curr = display._right - self.rect.width         
        if curr <= 0:                               
            curr = 0           
        self.rect.topleft = [curr, save]            #reassigns the X,Y to rect.topleft