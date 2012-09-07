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

class Goal(pygame.sprite.Sprite):
    def __init__(self, ip, map_xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = display.load_image("popcornstand.png", -1)
        self.rect.right = ip - map_xpos
        self.rect.top = (display.env.floor - self.rect.height)
        self.relative_xpos = ip
        self.bonus = 1,000,000
        self.next_update_time = 0
        self.value = 0

    def update(self, current_time, map_xpos, player_xy):
        if self.next_update_time <= current_time:
            self.rect.right = self.relative_xpos - map_xpos
        
            self.next_update_time = current_time + 10
    
    def die(self):
        return

map = Map()