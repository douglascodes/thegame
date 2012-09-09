import pygame

#create game groups
players = pygame.sprite.GroupSingle()   #player group
targs = pygame.sprite.Group()       #initiates the old lady group
clouds = pygame.sprite.Group()      #holds clouds
pshots = pygame.sprite.Group()      #holds all player projectiles
eshots = pygame.sprite.Group()      #holds all enemy projectiles
splashes = pygame.sprite.Group()    #holds all player projectiles
road = pygame.sprite.Group()        #group for the background/foreground stuff
numof_clouds = 8                    #how many clouds do we want