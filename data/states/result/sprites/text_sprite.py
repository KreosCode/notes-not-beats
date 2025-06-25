import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, font_size: int, font_color: str, pos: list):
        super().__init__()

        font = pygame.font.Font("src/fonts/metropolis.thin.otf", font_size)
        self.image = font.render(text, True, font_color)
        self.rect = self.image.get_rect(topleft = pos)