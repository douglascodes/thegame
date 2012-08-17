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

def check_hits():
    hits = pygame.sprite.groupcollide(p1.playershots_grp, ladies, False, False)
    for x in iter(hits):
        y = hits[x]
        x.die()
        y[0].die()

def check_cloud():
    if len(cloud_grp) < 6:
        cloud_grp.add(display.Cloud())
                                
pygame.display.flip()   

p1 = player.Player()
players = pygame.sprite.GroupSingle()       #intitates the singleton group for player
players.add(p1)                 #adds player 1 to the singleton group


ladies = pygame.sprite.Group()  #initiates the old lady group
numof_ladies = 2                #how many old ladies do we want
for x in range(0, numof_ladies):            #for each numof_ we make a random start for a lady
    ladies.add(targets.Oldlady(random.randrange(1, (display._right))))   #starts and oldlady random loc
cloud_grp = pygame.sprite.Group()
numof_clouds = 6                #how many clouds do we want
for x in range(0, numof_clouds):
    cloud_grp.add(display.Cloud())

def main():   
    while p1.health:
        display.screen.fill(BLUE)
        fpsClock.tick(30)   
        now = pygame.time.get_ticks()
        cloud_grp.update(now)
        cloud_grp.draw(screen)
        players.draw(screen)                #updates the Player 
        p1.show_health()
        ladies.update(now)
        ladies.draw(screen)
        p1.playershots_grp.update(now)      
        p1.playershots_grp.draw(screen)
        p1.splashes_grp.update(now)
        p1.splashes_grp.draw(screen)
        pygame.display.flip()
        check_key()
        check_hits()
        check_cloud()

main()