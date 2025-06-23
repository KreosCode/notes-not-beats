# it just lines, that shows where notes should be 
# when corresponding button is being pressed
# p.s note_lane gap between it walls = 60px

import pygame

class NoteCatcher(pygame.sprite.Sprite):
    def __init__(self, side, key_indicator_rect):
        # side and key_indicator_rect are getting
        # from key_indicator
        super().__init__()
        
        self.side = side
        self.image = pygame.surface.Surface((60, 5))
        self.image.fill("#b1c6dc")

        match self.side:
            case "left":
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect = self.image.get_rect(midright = key_indicator_rect.midleft)
            case "right":
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect = self.image.get_rect(midleft = key_indicator_rect.midright)
            case "top":
                self.rect = self.image.get_rect(midbottom = key_indicator_rect.midtop)
            case "bottom":
                self.rect = self.image.get_rect(midtop = key_indicator_rect.midbottom)

    def update(self):
        pass