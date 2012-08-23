import pygame, sys, os, display, missiles, main
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    image = None
    vert_state = 0
    horz_state = 0
    fire_timer = 0
       
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        if Player.image is None:
            Player.image, Player.rect = display.load_image("balloon.png", -1)
        
        self.image, self.rect = Player.image, Player.rect
        
        self.rect.topleft = main.initial_position            #sets the balloon start at ip 
        self.score = 0                                  #points total over game
        self.health = main.max_health                               #current health is 100
        self.traveled = 0                               #tracks game length
        self.points = 0                                 #points this round
        self.splashes_grp = pygame.sprite.Group()       #sprite group for splashes 
        self.hbarpos = (10,10)

    def update(self):
        main.screen.blit(self.image, self.rect)
    
    def die(self):                                  #sets death animation and
        pass
    
    def win(self):                                  #tabulates the round points
        self.score = self.traveled + self.points
    
    def fire_weapon(self):                          #drops a balloon
        main.shots_grp.add(missiles.Fire(self.rect.midbottom))

    def pop_splash(self, ip):                          #drops a balloon
        self.splashes_grp.add(missiles.Splash(ip))
       
    def check_health(self):                         #checks the players current health
        if self.health <= 0:
            self.health = 0
            self.die()                              #runs death if health is 0
        if self.health >= main.max_health:
            self.health = main.max_health        #if health bonus exceeds 100, set to 100
                        
    def adj_health(self, amount):                   #checks the players current health
        self.health += amount
        self.check_health()

    def show_health(self):
        main.screen.fill([255,0,0], ((self.hbarpos), (main.max_health, 20))) #fills h-bar with red
        main.screen.fill([0,255,0], ((self.hbarpos), (self.health, 20)))        
        #covers h-bar with current health in green. Red remaining at end. 
                                                            

        
    def move_vert(self, amount):                    #move the balloon vertically
        self.rect.top += amount                              #increments Y by AMOUNT
        if self.rect.top >= main.floor - self.rect.height:      #limits the movement to outside border
            self.rect.top = main.floor - self.rect.height
        if self.rect.top <= 0:
            self.rect.top = 0
#        self.adj_health(-10)
        
    def move_horz(self, amount):
        self.rect.left += amount                                #increments the X by AMOUNT
        if self.rect.left >= main.right - self.rect.width:  #limits the movement to outside border
            self.rect.left = main.right - self.rect.width         
        if self.rect.left <= 0:                               
            self.rect.left = 0           
#        self.adj_health(10)
