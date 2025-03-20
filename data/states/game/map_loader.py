import pygame
from center_indicator_sprite import CenterIndicator
from note_catcher_sprite import NoteCatcher
from note_lane_sprite import NoteLane
from note_sprite import Note

class MapLoader():
    def __init__(self, screen, **timings):
        # init of sprite groups
        self.center_group = pygame.sprite.GroupSingle(CenterIndicator(screen))
        self.note_catcher_group = pygame.sprite.Group(NoteCatcher("left", self.center_group.sprite.rect),
                                                      NoteCatcher("right", self.center_group.sprite.rect),
                                                      NoteCatcher("top", self.center_group.sprite.rect),
                                                      NoteCatcher("bottom", self.center_group.sprite.rect))
        

    def sprites_draw(self):
        # drawing sprite groups

    def sprites_update(self):
        pass

    def get_event(self, event):
        pass