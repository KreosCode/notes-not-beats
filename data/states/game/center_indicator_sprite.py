import pygame

class CenterIndicator(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        screen_size = {
            "width": screen.get_width(),
            "height": screen.get_height()
        }

        """
        need to do something with relative path here
        the problem is that path is going from main.py, not from center_indicator_sprite.py
        """
        self.image = pygame.image.load("src/sprites/center_indicator.png").convert_alpha()
        self.rect = self.image.get_rect(center = (screen_size["width"] / 2, screen_size["height"] / 2))

    def update(self):
        pass