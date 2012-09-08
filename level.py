import display, pygame, collections
class Map():
    def __init__(self): 
        self.length = 5000
        self.pos = 0.0
        self.pbarpos = (0,0)
        self.spawn_list = []
        self.moving = True
        self.next_enemy = (0,0)
         
    def update(self):
        self.pbar = int(display.env.right * (self.pos/ self.length))
        display.env.screen.fill([240,240,0], ((self.pbarpos), (self.pbar, 20)))  #fills p-bar with yellow

        if self.pos <= self.length:
            self.pos += display.env.windspeed
        else: 
            self.moving = False

map = Map()