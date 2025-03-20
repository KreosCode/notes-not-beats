import pygame

class NoteLane(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface, catcher_type: str, catcher_rect: pygame.rect.Rect):
        super().__init__()
        self.image = pygame.image.load("src/sprites/note_lane.png").convert_alpha()

        match catcher_type:
            case "left":
                lane_length = catcher_rect.centerx
                self.image = pygame.transform.rotate(self.image, 90)
                self.image = pygame.transform.scale(self.image, (lane_length, self.image.get_height()))
                self.rect = self.image.get_rect(midleft = (0, catcher_rect.centery))
            case "right":
                lane_length = screen.get_width() - catcher_rect.centerx
                self.image = pygame.transform.rotate(self.image, 90)
                self.image = pygame.transform.scale(self.image, (lane_length, self.image.get_height()))
                self.rect = self.image.get_rect(midright = (screen.get_width(), catcher_rect.centery))
            case "top":
                lane_length = catcher_rect.centery
                self.image = pygame.transform.scale(self.image, (self.image.get_width(), lane_length))
                self.rect = self.image.get_rect(midtop = (catcher_rect.centerx, 0))
            case "bottom":
                lane_length = screen.get_height() - catcher_rect.centery
                self.image = pygame.transform.scale(self.image, (self.image.get_width(), lane_length))
                self.rect = self.image.get_rect(midbottom = (catcher_rect.centerx, screen.get_height()))
        

    def update(self):
        pass