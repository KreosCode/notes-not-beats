# show which key is being pressed atm

import pygame

class KeyIndicator(pygame.sprite.Sprite):
    def __init__(self, side, center_rect: pygame.rect.Rect):
        super().__init__()

        self.side = side
        margin = 5 # in pixels
        self.image = pygame.image.load("src/sprites/key_indicator.png").convert_alpha()

        match self.side:
            case "left":
                self.rect = self.image.get_rect(midright = (center_rect.midleft))
                self.rect.x -= margin
            case "right":
                self.rect = self.image.get_rect(midleft = (center_rect.midright))
                self.rect.x += margin
            case "top":
                self.rect = self.image.get_rect(midbottom = (center_rect.midtop))
                self.rect.y -= margin
            case "bottom":
                self.rect = self.image.get_rect(midtop = (center_rect.midbottom))
                self.rect.y += margin
            case _:
                print("Wrong side provided")

    def on_press(self):
        self.image = pygame.image.load("src/sprites/key_indicator_pressed.png").convert_alpha()

    def update(self, pressed):
        if pressed:
            self.on_press()
        else:
            self.image = pygame.image.load("src/sprites/key_indicator.png").convert_alpha()