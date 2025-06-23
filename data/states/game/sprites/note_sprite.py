# IMPORTANT:
# end_timing1 of next object has to be more then end_timing2 (if slider)/end_timing1 (if single)

import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, dt, note_lane_rect, distance, speed, **timings):
        """
        types of timings kwargs:
        note - 1: {'type': 'single', 'sound_name1': 'soft-hitwhistle2.wav', 'end_timing1': '2660', 'side': 'top'}
        slider - 2: {'type': 'slider', 'sound_name1': 'soft-hitwhistle2.wav', 'sound_name2': 'pause', 'end_timing1': '3035', 'end_timing2': '3597', 'side': 'right'}
        """
        super().__init__()
        self.id = next(iter(timings))
        self.__dict__.update(timings[self.id])
        self.speed = speed
        
        match self.type:
            case 'single':
                self.image = pygame.image.load('src/sprites/note.png').convert_alpha()
                
                match self.side:
                    case 'left':
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(midleft = note_lane_rect.midleft)
                    case 'right':
                        self.image = pygame.transform.rotate(self.image, -90)
                        self.rect = self.image.get_rect(midright = note_lane_rect.midright)
                    case 'top':
                        self.rect = self.image.get_rect(midbottom = note_lane_rect.midtop)
                    case 'bottom':
                        self.rect = self.image.get_rect(midtop = note_lane_rect.midbottom)
        
            
    def move(self):
        if self.side == "left":
            self.rect.x += self.speed
        if self.side == "right":
            self.rect.x -= self.speed
        if self.side == "top":
            self.rect.y += self.speed
        if self.side == "bottom":
            self.rect.y -= self.speed

    def update(self):
        self.move()