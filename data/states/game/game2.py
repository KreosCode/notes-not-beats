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

        # maybe move all following part in the startup?

        self.bg_color = "#010203"
        self.sprite_assigned = False      # indicates if sprite_assign() is executed

        # game constants
        self.APPROACH_TIME = 2000 # 

        # vvv Temporary part (parsing)
        path = "songs/Onoken - Sagashi Mono/sagashi_mono.nnb"
        self.song_general_info = config_loader.option_load(path, False)["[General]"]
        # self.song_difficulty_info = config_loader.option_load("songs/Onoken - Sagashi Mono/sagashi_mono.nnb", False)["[Difficulty]"]
        # self.song_timing_options_info = config_loader.option_load("songs/Onoken - Sagashi Mono/sagashi_mono.nnb", False)["[TimingOptions]"]
        self.song_note_timings = config_loader.option_load(path, True)["[NoteTimings]"]
        # ^^^ Temporary part (parsing)

        self.keybinds = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "top": pygame.K_w,
            "bottom": pygame.K_s
        }

    def startup(self):
        pass

    def cleanup(self):
        # 'unpressing' all indicators
        for sprite in self.key_indicators.sprites():
            sprite.update(pressed = False)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE:
               self.done = True

           # changing key_indicator sprite if
           # corresponding key is being pressed
           for action, keybind in self.keybinds.items():
                if event.key == keybind:
                    for sprite in self.key_indicators.sprites():
                        if sprite.side == action:
                            sprite.update(pressed = True)

        if event.type == pygame.KEYUP:
           # changing key_indicator sprite if
           # corresponding key is being unpressed
           for action, keybind in self.keybinds.items():
                if event.key == keybind:
                    for sprite in self.key_indicators.sprites():
                        if sprite.side == action:
                            sprite.update(pressed = False)

    def update(self, screen, dt):
        screen.fill(self.bg_color)          # updating background

        if not self.sprite_assigned:        # assigning sprites to their groups
            self.sprite_assign(screen)
            self.sprite_assigned = True
        
        self.notes.update()
        self.draw(screen)

    def draw(self, screen):
        self.note_lane.draw(screen)
        self.notes.draw(screen)
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

        # distance between screen edge and catcher (same for all sides)
        for sprite in self.note_catcher.sprites():
            if sprite.side == 'top':
                distance = sprite.rect.top

        self.center_background = pygame.sprite.GroupSingle(CenterBackground(self.center_indicator.sprite.rect,
                                                                            self.bg_color))
        
        self.notes = pygame.sprite.Group()