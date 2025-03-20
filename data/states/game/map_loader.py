import pygame
from center_indicator_sprite import CenterIndicator
from center_background_sprite import CenterBackground
from note_catcher_sprite import NoteCatcher
from note_lane_sprite import NoteLane   
from note_sprite import Note

class MapLoader():
    def __init__(self, screen:pygame.surface.Surface, **timings):
        self.screen = screen

        # init of sprite groups
        self.center_group = pygame.sprite.GroupSingle(CenterIndicator(screen))

        self.note_catcher_group = pygame.sprite.Group()
        self.note_catcher_list = []
        for side in ("left", "right", "top", "bottom"):
            self.note_catcher_group.add(NoteCatcher(side, self.center_group.sprite.rect))

        self.note_lane_group = pygame.sprite.Group()
        for sprite in self.note_catcher_group.sprites():
            self.note_lane_group.add(NoteLane(screen, sprite.type, sprite.rect))
            self.note_catcher_list.append(sprite)

        self.center_background_group = pygame.sprite.GroupSingle(CenterBackground(self.note_catcher_list))

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