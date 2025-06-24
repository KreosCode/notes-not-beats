# IMPORTANT:
# end_timing1 of next object has to be more then end_timing2 (if slider)/end_timing1 (if single)

import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, note_lane_rect, approach_time, distance, spawn_time, type, sound_name1, end_timing1, side):
        """
        types of timings kwargs:
        note - {'type': 'single', 'sound_name1': 'soft-hitwhistle2.wav', 'end_timing1': '2660', 'side': 'top'}
        slider - {'type': 'slider', 'sound_name1': 'soft-hitwhistle2.wav', 'sound_name2': 'pause', 'end_timing1': '3035', 'end_timing2': '3597', 'side': 'right'}
        """
        super().__init__()
        self.spawn_time = spawn_time
        self.type = type
        self.sound_name1 = sound_name1
        self.end_timing1 = end_timing1
        self.side = side
        
        self.velocity = distance / approach_time

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

    def update(self, dt):
        # velocity = px/ms, dt = ms/frame
        px_per_frame = self.velocity * dt
        match self.side:
            case 'left':
                self.rect.x += px_per_frame
            case 'right':
                self.rect.x -= px_per_frame
            case 'top':
                self.rect.y += px_per_frame
            case 'bottom':
                self.rect.y -= px_per_frame