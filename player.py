import pygame, sys, os, display, missiles, groups, level
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image, self.rect = display.load_image("balloon.png", -1)
        
        self.rect.topleft = display.env.initial_position    #sets the balloon start at IP 
        self.score = 0                                      #points total over game
        self.points = 0                                     #points this round
        self.health = display.env.max_health                #current health is 100
        self.hbarpos = (0,20)                               #Health bar initial position
#        self.pause_map = False                              #used for testing

        self.vert_state = 0
        self.horz_state = 0
        self.fire_timer = 0


    def update(self):
        display.env.screen.blit(self.image, self.rect)
    
    def die(self):                                  #sets death animation and
        pass
    
    def win(self):                                  #tabulates the round points
        self.score = int(level.map.pos) + self.points # + level.map.bonus
        #increases successful level points plus distance traveled. + hitting goal bonus 
        self.points = 0
    
    def fire_weapon(self):                          #drops a balloon
#        self.pause_map = not self.pause_map
#        if self.pause_map:
#            display.env.windspeed = 0
#        else:
#            display.env.windspeed = 10
        groups.pshots.add(missiles.Fire(self.rect.midbottom))

    def check_health(self):                         #checks the players current health
        if self.health <= 0:
            self.health = 0
            self.die()                              #runs death if health is 0
        if self.health >= display.env.max_health:
            self.health = display.env.max_health        #if health bonus exceeds 100, set to 100
                        
    def adj_health(self, amount):                   #checks the players current health
        self.health += amount
        self.check_health()

    def adj_score(self, amount):                   #checks the players current health
        self.points += amount
        print self.points

    def show_health(self):
        display.env.screen.fill([255,0,0], ((self.hbarpos), (display.env.max_health, 20)))    #fills h-bar with red
        display.env.screen.fill([0,255,0], ((self.hbarpos), (self.health, 20)))        
        #covers h-bar with current health in green. Red remaining at end. 
                                                            
    def move_vert(self, amount):                            #move the balloon vertically
        self.rect.top += amount                             #increments Y by AMOUNT
        if self.rect.top >= display.env.floor - self.rect.height:  #limits the movement to outside border
            self.rect.top = display.env.floor - self.rect.height
        if self.rect.top <= 0:
            self.rect.top = 0
#        self.adj_health(-10)
        
    def move_horz(self, amount):
        self.rect.left += amount                                #increments the X by AMOUNT
        if self.rect.left >= display.env.right - self.rect.width:  #limits the movement to outside border
            self.rect.left = display.env.right - self.rect.width         
        if self.rect.left <= 0:                               
            self.rect.left = 0           
#        self.adj_health(10)

p1 = Player() #Creates the player character, know as P1
groups.players.add(p1)