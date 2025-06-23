import pygame

class CenterBackground(pygame.sprite.Sprite):
    def __init__(self, center_rect, bg_color):
        super().__init__()
        # SUPER TEMPORARY, CHANGE IT LATER
        horizontal_image = pygame.surface.Surface((72, center_rect.height))
        horizontal_image.fill(bg_color)
        vertical_image = pygame.surface.Surface((center_rect.width, 72))
        vertical_image.fill(bg_color)

        self.image = pygame.surface.Surface((horizontal_image.get_width(), vertical_image.get_height()))
        self.image.blits(((horizontal_image, (0, self.image.get_height()/2 - horizontal_image.get_height()/2)),
                         (vertical_image, (self.image.get_width()/2 - vertical_image.get_width()/2, 0))))
        self.image.set_colorkey('#000000')
        self.rect = self.image.get_rect(center = center_rect.center)