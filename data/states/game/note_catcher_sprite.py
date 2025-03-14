import pygame

class NoteCatcher(pygame.sprite.Sprite):
    def __init__(self, type, **center_params):
        super().__init__()

        self.__dict__.update(center_params)
        self.type = type
        self.padding = 10 # in pixels
        """
        need to do something with relative path here
        the problem is that path is going from main.py, not from center_indicator_sprite.py
        """
        self.image = pygame.image.load("src/sprites/note_catcher.png").convert_alpha()

        match self.type:
            case "left":
                self.rect = self.image.get_rect(midright = (self.center_midleft))
                self.rect.x -= self.padding
            case "right":
                self.rect = self.image.get_rect(midleft = (self.center_midright))
                self.rect.x += self.padding
            case "top":
                self.rect = self.image.get_rect(midbottom = (self.center_midtop))
                self.rect.y -= self.padding
            case "bottom":
                self.rect = self.image.get_rect(midtop = (self.center_midbottom))
                self.rect.y += self.padding
            case _:
                print("Wrong type provided")

    def pressed(self):
        self.image = pygame.image.load("src/sprites/note_catcher_pressed.png").convert_alpha()

    def update(self, pressed):
        if pressed:
            self.pressed()
        else:
            self.image = pygame.image.load("src/sprites/note_catcher.png").convert_alpha()