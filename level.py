import display, pygame, collections
class Map():                            #as map generation expands this will accept arg from main
    def __init__(self): 
        self.length = 5000              #Default map length. Eventually this will be an arg
        self.pos = 0.0                  #Float for current map pos. Starts at zero
        self.pbarpos = (0,0)            #Progress bar graphic x,y position
        self.spawn_list = []            #Place to keep the spawn list
        self.moving = True              #Boolean for setting the map movement to stop
        self.next_enemy = (0,0)         #Tuple for holding the next spawn from the list
         
    def update(self):
        self.pbar = int(display.env.right * (self.pos/ self.length))    
        #Calculate the progress length, believe it must be an INT to function correct in pygame
        display.env.screen.fill([240,240,0], ((self.pbarpos), (self.pbar, 20)))  #fills p-bar with yellow

        if self.pos <= self.length:             #If map is not at the end
            self.pos += display.env.windspeed   #Moves the current map position by windspeed
        else: 
            self.moving = False                 #Sets map movement to stop (not used currently)

map = Map()