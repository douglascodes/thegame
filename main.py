import pygame, sys, os, player, display, missiles, targets, random
from pygame.locals import *

#Sets up some global variables, mostly based on the display module's attrib

scale = 256
bottom = scale * 3
right = scale * 4
BLUE = (135, 199, 218)
BLACK = (0,0,0)
initial_position = [100, 100]
floor = bottom - 64
windspeed = 5
max_health = 300
step = 15
clock = fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((right, bottom))
looptime = 30
pygame.key.set_repeat(1, looptime)
fire_delay = 1000
rand = random.randrange

pygame.init()

def exit_game(): 
    pygame.quit()
    os._exit(0)
   
def check_key():
    #check the keyboard input for one of the following: SPACE, ESC, UP, DOWN, LEFT, RIGHT
    #this first section increments the balloon left/right and up/down, based on the Vert/Horz states
    #if the players movement states are not == 0, then it operates.
    #Multiplying by the "State" turns the number negative or positive. Therefore fitting
    # to the move "amount" statements under the player move methods.  
    if p1.horz_state != False:                               
        p1.move_horz(step * p1.horz_state)
    if p1.vert_state != False:
        p1.move_vert(step * p1.vert_state)
    
    #Keydown states either escape, fire or set the move Dirs.
    #This allows the movement simultaneously of horizontal and vertical
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: exit_game()
            if event.key == K_UP: p1.vert_state = -1    #The negative modifier is applied for UP
            if event.key == K_DOWN: p1.vert_state = 1   #The positive modifier for down
            if event.key == K_LEFT: p1.horz_state = -1  #The negative is applied for LEFT
            if event.key == K_RIGHT: p1.horz_state = 1  #The positive is applied for DOWN
            if event.key == K_SPACE and p1.fire_timer < pygame.time.get_ticks():
                p1.fire_weapon()
                p1.fire_timer = pygame.time.get_ticks() + fire_delay
        #It would be silly to fire off unlimited water balloons. So it has a delay, set in 
        #the display module. The "fire_timer" is an attribute of the player class.
                        
        if event.type == KEYUP:     #Setting to ZERO makes the states FALSE.
            if event.key == K_UP: p1.vert_state = 0  
            if event.key == K_DOWN: p1.vert_state = 0
            if event.key == K_LEFT: p1.horz_state = 0
            if event.key == K_RIGHT: p1.horz_state = 0
        #The release of any arrow key ceases movement of its axis.
        
            
def check_hits():   #Collision detection between the ladies and balloon drops
    hits = pygame.sprite.groupcollide(shots_grp, targs_grp, False, False) #Adds collisions to hits
    for x in iter(hits):                #Searches over the collision dictionary
        y = hits[x]                     #X and Y are the collision. X is key to Y.
        x.die()                         #Runs the die() method in object X
        y[0].die()                      #Runs the die() method in object Y. It's a list for some reason.

    hits = pygame.sprite.groupcollide(shots_grp, players, False, False) #Adds collisions to hits
    for x in iter(hits):                #Searches over the collision dictionary
        y = hits[x]                     #X and Y are the collision. X is key to Y.
        y[0].adj_health(-x.power)       #adjusts the player health
        x.die()                         #Runs the die() method in object X


def check_cloud():                      #Maintains the level of clouds
    if len(cloud_grp) < numof_clouds:   #Respawns clouds if there are less than expected.
        cloud_grp.add(display.Cloud())  #Adds the new clouds to the group
                                
pygame.display.flip()   

p1 = player.Player()                        #Creates the player character, know as P1
players = pygame.sprite.GroupSingle()       #intitates the singleton group for player
players.add(p1)                             #adds player 1 to the singleton group

targs_grp = pygame.sprite.Group()               #initiates the old lady group
targs_grp.add(targets.Guard(rand(1, (right))))  #starts and oldlady random loc

cloud_grp = pygame.sprite.Group()   #holds clouds
shots_grp = pygame.sprite.Group()   #holds all projectiles
numof_clouds = 7                    #how many clouds do we want

for x in range(numof_clouds):       #creates clouds per numof_coulds
    cloud_grp.add(display.Cloud())  #adds em to cloud grp
road = pygame.sprite.GroupSingle()  #singular group for the Road/Path
g = display.Ground()                #Creates the ground object known as G
road.add(g)                         #Adds g to single group for ground

def game():   
    while p1.health:                #Game continues while P1 is alive
        screen.fill(BLUE)           #fills the background with named color
        fpsClock.tick(looptime)         #Paces the game to 30 fps
        now = pygame.time.get_ticks()   #sets 'NOW' to ... well... now
        cloud_grp.update(now)           #passes the current time to the cloud update group
        cloud_grp.draw(screen)          #draws the clouds to screen
        road.update()                   #Updates the single group 'road', no time is needed. Based on pos
        road.draw(screen)               #Draws the road
        players.draw(screen)            #updates the Player 
        p1.show_health()                #Dislays the health bar
        targs_grp.update(now)           #Makes the targs_grp move
        targs_grp.draw(screen)          #Draws em to the screen
        shots_grp.update(now)           #Updates the balloon drops
        shots_grp.draw(screen)          #Draws em to screen
        p1.splashes_grp.update(now)     #Updates the splashes states
        p1.splashes_grp.draw(screen)    #Draws em
        pygame.display.flip()           #Draws the screen
        check_key()                     #Looks for key presses/unpress
        check_hits()                    #Checks collision between appropriate groups
        check_cloud()                   #Continues to spawn background clouds as necc.

game()  #Runs the game.