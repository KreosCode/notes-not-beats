import pygame

class NoteLane(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        lane = pygame.image.load("src/sprites/note_lane.png").convert_alpha()
        vertical_lane = pygame.transform.scale(lane, (lane.get_width(), screen.get_height()))
        horizontal_lane = pygame.transform.rotate(lane, 90)
        horizontal_lane = pygame.transform.scale(horizontal_lane, (screen.get_width(), horizontal_lane.get_height()))
        """file path..."""
        self.image = pygame.Surface(screen.get_size())
        self.image.blits(blit_sequence=[(vertical_lane, (screen.get_width() / 2 - vertical_lane.get_width() / 2, 0)), 
                                        (horizontal_lane, (0, screen.get_height() / 2 - horizontal_lane.get_height() / 2))])
        """____________"""
        self.rect = self.image.get_rect()
    def update(self):
        pass
        