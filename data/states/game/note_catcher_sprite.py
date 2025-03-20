import pygame

class NoteCatcher(pygame.sprite.Sprite):
    def __init__(self, type, center_rect: pygame.rect.Rect):
        super().__init__()

        self.type = type
        margin = 10 # in pixels
        """
        need to do something with relative path here
        the problem is that path is going from main.py, not from center_indicator_sprite.py
        """
        self.image = pygame.image.load("src/sprites/note_catcher.png").convert_alpha()

        match self.type:
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
                print("Wrong type provided")

    def pressed(self):
        self.image = pygame.image.load("src/sprites/note_catcher_pressed.png").convert_alpha()

    def update(self, pressed):
        if pressed:
            self.pressed()
        else:
            self.image = pygame.image.load("src/sprites/note_catcher.png").convert_alpha()