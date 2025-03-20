import pygame
from center_indicator_sprite import CenterIndicator
from note_catcher_sprite import NoteCatcher
from note_lane_sprite import NoteLane
from note_sprite import Note

class MapLoader():
    def __init__(self, screen, **timings):
        # init of sprite groups
        self.center_group = pygame.sprite.GroupSingle(CenterIndicator(screen))

        self.note_catcher_group = pygame.sprite.Group()
        for side in ("left", "right", "top", "bottom"):
            self.note_catcher_group.add(side, self.center_group.sprite.rect)

        self.note_lane_group = pygame.sprite.Group()
        for sprite in self.note_catcher_group.sprites():
            self.note_lane_group.add(NoteLane(screen, sprite.type, sprite.rect))

        self.note_group = pygame.sprite.Group()
        

    def sprites_draw(self):
        # drawing sprite groups
        self.center_group.draw()
        self.note_catcher_group.draw()
        self.note_lane_group.draw()

    def sprites_update(self):
        pass

    def get_event(self, event):
        pass