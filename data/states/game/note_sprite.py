import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, type, side, sound_name1, sound_name2 = None):
        super().__init__()

