import pygame, sys, os, player, display, missiles, targets, random
from pygame.locals import *

step = display.step
pygame.init()
BLUE = display.BLUE
BLACK = display.BLACK
clock = fpsClock = pygame.time.Clock()
scale = display.scale
_bottom = scale * 3
_right = scale * 4
screen = pygame.display.set_mode((_right, _bottom))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLUE)
initial_position = display.initial_position
#players = pygame.sprite.Group()


class Obstacle:
    pass

class AirObs (Obstacle):
    pass

class LandObs (Obstacle):
    pass

class Goal:
    x = 10
    y = 100
    bonus = 1,000,000
    pass

class Map:
    length = 1000
    pass


def exit_game():
    pygame.quit()
    os._exit(0)
   
def check_key():
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: exit_game()
            elif event.key == K_UP: p1.move_vert(-step)
            elif event.key == K_DOWN: p1.move_vert(step)
            elif event.key == K_LEFT: p1.move_horz(-step)
            elif event.key == K_RIGHT: p1.move_horz(step)
            elif event.key == K_SPACE:
                p1.fire_weapon()
                                
pygame.display.flip()   

p1 = player.Player()
players = pygame.sprite.GroupSingle()       #intitates the singleton group for player
players.add(p1)                 #adds player 1 to the singleton group


l1 = []                         #list to be passed to the old lady group
numof_ladies = 3                #how many old ladies do we want
for x in range(0, numof_ladies):            #for each numof_ we make a random start for a lady
    l1.append(targets.Oldlady(random.randrange(1, (display._right))))   #starts and oldlady random loc
ladies = pygame.sprite.Group()  #initiates the old lady group
ladies.add(l1)                  #adds the list of oldlady objects to the group



def main():   
    while p1.health:
        display.screen.fill(BLUE)
        fpsClock.tick(30)   
        now = pygame.time.get_ticks()
        players.draw(screen)                #updates the Player 
        ladies.draw(screen)
        ladies.update(now)
        p1.playershots_grp.update(now)      
        p1.playershots_grp.draw(screen)
        p1.splashes_grp.update(now)
        p1.splashes_grp.draw(screen)
        pygame.display.flip()
        check_key()

main()