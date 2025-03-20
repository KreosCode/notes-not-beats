import pygame

class CenterBackground(pygame.sprite.Sprite):
    def __init__(self, catcher_list):
        super().__init__()
        # catcher_list = ["left", "right", "top", "bottom"]
        size = (catcher_list[1].rect.centerx - catcher_list[0].rect.centerx,
                catcher_list[3].rect.centery - catcher_list[2].rect.centery)
        
        self.image = pygame.surface.Surface(size)
        self.rect = self.image.get_rect(topleft = (catcher_list[0].rect.centerx, catcher_list[2].rect.centery))