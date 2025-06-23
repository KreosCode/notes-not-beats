import pygame

class CenterIndicator(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface):
        super().__init__()
        self.margin = 5 # px, affects on key_indicators
        self.image = pygame.image.load("src/sprites/center_indicator.png").convert_alpha()
        self.rect = self.image.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2))

    def update(self):
        pass