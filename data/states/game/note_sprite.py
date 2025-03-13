import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, type, **timings):
        super().__init__()
        self.__dict__.update(timings)

        if type == "single":
            self.image = 
        if type == "slider":
            pass