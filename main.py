import pygame, os, display, player, groups, missiles, targets, random, level
from pygame.locals import *

def exit_game(): 
    pygame.quit()
    os._exit(0)
   
def check_key():
    #check the keyboard input for one of the following: SPACE, ESC, UP, DOWN, LEFT, RIGHT
    #this first section increments the balloon left/right and up/down, based on the Vert/Horz states
    #if the players movement states are not == 0, then it operates.
    #Multiplying by the "State" turns the number negative or positive. Therefore fitting
    # to the move "amount" statements under the player move methods.  
    if player.p1.horz_state:                               
        player.p1.move_horz(display.env.step * player.p1.horz_state)
    if player.p1.vert_state:
        player.p1.move_vert(display.env.step * player.p1.vert_state)
    
    #Keydown states either escape, fire or set the move Dirs.
    #This allows the movement simultaneously of horizontal and vertical
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: exit_game()
            if event.key == K_UP: player.p1.vert_state = -1    #The negative modifier is applied for UP
            if event.key == K_DOWN: player.p1.vert_state = 1   #The positive modifier for down
            if event.key == K_LEFT: player.p1.horz_state = -1  #The negative is applied for LEFT
            if event.key == K_RIGHT: player.p1.horz_state = 1  #The positive is applied for DOWN
            if event.key == K_SPACE and player.p1.fire_timer < pygame.time.get_ticks():
                player.p1.fire_weapon()
                player.p1.fire_timer = pygame.time.get_ticks() + display.env.fire_delay
        #It would be silly to fire off unlimited water balloons. So it has a delay, set in 
        #the display module. The "fire_timer" is an attribute of the player class.
                        
        if event.type == KEYUP:     #Setting to ZERO makes the states FALSE.
            if event.key == K_UP or event.key == K_DOWN: player.p1.vert_state = 0  
            if event.key == K_LEFT or event.key == K_RIGHT : player.p1.horz_state = 0
        #The release of any arrow key ceases movement of its axis.
        
            
def check_hits():   #Collision detection between the ladies and balloon drops
    hits = pygame.sprite.groupcollide(groups.pshots, groups.targs, False, False) #Adds collisions to hits
    for x in iter(hits):                #Searches over the collision dictionary
        y = hits[x]                     #X and Y are the collision. X is key to Y.
        x.die()                         #Runs the die() method in object X
        for z in y:
            if z.value > 0: player.p1.adj_score(z.value)
            z.die()                      #Runs the die() method in object Y. It's a list for some reason.

    hits = pygame.sprite.groupcollide(groups.eshots, groups.players, False, False) #Adds collisions to hits
    for x in iter(hits):                #Searches over the collision dictionary
        y = hits[x]                     #X and Y are the collision. X is key to Y.
        x.die()                         #Runs the die() method in object X
        #y[0].adj_health(-x.power)       #adjusts the player health


def check_cloud():                      #Maintains the level of clouds
    while len(groups.clouds) < groups.numof_clouds:   #Respawns clouds if there are less than expected.
        groups.clouds.add(display.Cloud())  #Adds the new clouds to the group

def populate(curr_map):
    for x in range(groups.numof_clouds):       #creates clouds per numof_coulds
        groups.clouds.add(display.Cloud())     #adds em to cloud group
    
    enemy_count = curr_map.length / display.env.scale
    kinds = ["None", "Oldlady", "Guard", "Goal"]
    for x in range(enemy_count): 
        pos = rand(curr_map.pos, curr_map.length)
        kind = kinds[rand(len(kinds)-1)]
        curr_map.spawn_list.append([pos, kind])

    curr_map.spawn_list.append([curr_map.length + (display.env.scale * 3), "Goal"])   #adds a goal to the end of map
    curr_map.spawn_list = sorted(curr_map.spawn_list)       #Sorts the spawn_list
    curr_map.next_spawn = curr_map.spawn_list.pop(0)        #
    curr_map.spawn_list.append([curr_map.length, "END"])   #Terminus to spawns

   
def spawn(curr_map):
    if curr_map.next_spawn[1] == "END": return
    
    while curr_map.next_spawn[0] < curr_map.pos + display.env.right + display.env.scale * 2:
        if curr_map.next_spawn[1] == "Guard": groups.targs.add(targets.Guard(curr_map.next_spawn[0], curr_map.pos))
        elif curr_map.next_spawn[1] == "Oldlady": groups.targs.add(targets.Oldlady(curr_map.next_spawn[0], curr_map.pos))
        elif curr_map.next_spawn[1] == "Goal": groups.targs.add(targets.Goal(curr_map.next_spawn[0], curr_map.pos))
        try:
            curr_map.next_spawn = curr_map.spawn_list.pop(0)
        except:
            print "Empty spawn list."
            return

def map_end():
    exit_game()
                                
def game():   
    clock = pygame.time.Clock()
    screen = display.env.screen
    curr_map = level.map
    populate(curr_map)
    curr_map.next_spawn = curr_map.spawn_list.pop(0)
    while player.p1.health:                #Game continues while P1 is alive
        spawn(curr_map)           
        display.env.screen.fill(display.env.BLUE)           #fills the background with named color
        clock.tick(display.env.looptime)         #Paces the game to 30 fps
        now = pygame.time.get_ticks()       #sets 'NOW' to ... well... now
        groups.clouds.update(now)           #passes the current time to the cloud update group
        groups.clouds.draw(screen)          #draws the clouds to screen
        curr_map.update()
        groups.road.update(curr_map.moving)    #Updates the single group 'road', no time is needed. Based on pos
        groups.road.draw(screen)               #Draws the road
        groups.players.draw(screen)            #updates the Player 
        player.p1.show_health()                #Displays the health bar
        groups.targs.update(now, curr_map.pos, player.p1.rect.midtop) #Makes the targs_grp move, needs player for shooting back
        groups.targs.draw(screen)          #Draws em to the screen
        groups.pshots.update(now)           #Updates the balloon drops
        groups.pshots.draw(screen)          #Draws em to screen
        groups.eshots.update(now)           #Updates the enemy shots
        groups.eshots.draw(screen)          #Draws em to screen
        groups.splashes.update(now)     #Updates the splashes states
        groups.splashes.draw(screen)    #Draws em
        pygame.display.flip()           #Draws the screen
        check_key()                     #Looks for key presses/unpress
        check_hits()                    #Checks collision between appropriate groups
        check_cloud()                   #Continues to spawn background clouds as necc.

rand = random.randrange

game()  #Runs the game.