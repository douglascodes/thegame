from pygame.sprite import RenderClear

class OrderedRenderUpdates(RenderClear):
    def __init__(self, group = ()):
        self.spritelist = []
        RenderClear.__init__(self, group)
        
    def sprites(self):
        return self.spritelist[:]
    
    def add(self, sprite):
        if hasattr(sprite, '_spritegroup'):
            for sprite in sprite.sprites():
                if sprite not in self.spritedict:
                    self.add_internal(sprite)
                    sprite.add_internal(self)
        else:
            try: len(sprite)
            except (TypeError, AttributeError):
                if sprite not in self.spritedict:
                    self.add_internal(sprite)
                    sprite.add_internal(self)
            else:
                for sprite in sprite:
                    if sprite not in self.spritedict:
                        self.add_internal(sprite)
                        sprite.add_internal(self)
        
    def add_internal(self, sprite):
        RenderClear.add_internal(self, sprite)
        self.spritelist.append(sprite)
        
    def remove_internal(self, sprite):
        RenderClear.remove_internal(self, sprite)
        self.spritelist.remove(sprite)
        
    def draw(self, surface):
        spritelist = self.spritelist
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in spritelist:
            r = spritedict[s]
            newrect = surface_blit(s.image, s.rect)
            if r is 0:
                dirty_append(newrect)
            else:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
            spritedict[s] = newrect
        return dirty

    