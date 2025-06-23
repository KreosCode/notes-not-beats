# In this state the main game is happening:
# notes being spawned, music being played etc

import pygame
from ...state import States
from .sprites.center_background_sprite import CenterBackground
from .sprites.center_indicator_sprite import CenterIndicator
from .sprites.key_indicator_sprite import KeyIndicator
from .sprites.note_catcher_sprite import NoteCatcher
from .sprites.note_lane_sprite import NoteLane
from .sprites.note_sprite import Note
from . import config_loader

class Game2(States):
    def __init__(self):
        super().__init__()
        self.next = "menu"

        self.bg_color = "#010203"

        self.sprite_assigned = False      # indicates if sprite_assign() is executed

    def startup(self):
        pass

    def cleanup(self):
        pass

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        screen.fill(self.bg_color)          # updating background

        if not self.sprite_assigned:        # assigning sprites to their groups
            self.sprite_assign(screen)
            self.sprite_assigned = True
        
        self.draw(screen)

    def draw(self, screen):
        self.note_lane.draw(screen)
        # add note sprite here
        self.center_background.draw(screen)
        self.center_indicator.draw(screen)
        self.key_indicators.draw(screen)
        self.note_catcher.draw(screen)

    def sprite_assign(self, screen):
        self.note_lane = pygame.sprite.GroupSingle(NoteLane(screen))
        self.center_indicator = pygame.sprite.GroupSingle(CenterIndicator(screen))
        self.key_indicators = pygame.sprite.Group()
        for side in ('left', 'right', 'top', 'bottom'):
            self.key_indicators.add(KeyIndicator(side, self.center_indicator.sprite.rect, self.center_indicator.sprite.margin))

        self.note_catcher = pygame.sprite.Group()
        for sprite in self.key_indicators.sprites():
            self.note_catcher.add(NoteCatcher(sprite.side, sprite.rect))

        self.center_background = pygame.sprite.GroupSingle(CenterBackground(self.center_indicator.sprite.rect,
                                                                            self.bg_color))