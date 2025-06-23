# In this state the main game is happening:
# notes being spawned, music being played etc

import pygame
from ...state import States
from .center_indicator_sprite import CenterIndicator
from .note_catcher_sprite import NoteCatcher
from .note_lane_sprite import NoteLane
from .note_sprite import Note
from . import config_loader

class Game2(States):
    def __init__(self):
        super().__init__()
        self.next = "menu"

        self.bg_color = "#010203"

        self.drawn_once = False           # indicates if draw_once() is executed
        self.sprite_assigned = False      # indicates if sprite_assign() is executed

    def startup(self):
        pass

    def cleanup(self):
        pass

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        if not self.updated_once:
            self.draw_once(screen)
            self.drawn_once = True

    def draw_once(self, screen):
        screen.fill(self.bg_color)          # setting background    

    def draw(self, screen):
        pass

    def sprite_assign(self, screen):
        pass