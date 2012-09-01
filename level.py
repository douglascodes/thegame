import display, collections
class Map():
    def __init__(self): 
        self.length = 10000
        self.pos = 0.0
        self.pbarpos = (0,0)
        self.enemies = []
        self.next_enemy = (0,0)
        
    def update(self):
        self.pbar = int(display.env.right * (self.pos/ self.length))
        display.env.screen.fill([240,240,0], ((self.pbarpos), (self.pbar, 20)))  #fills h-bar with red

        if self.pos <= self.length:
            self.pos += display.env.windspeed
        else: return

class Goal():
    x = 10
    y = 100
    bonus = 1,000,000
    pass

map = Map()