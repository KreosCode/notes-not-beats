import pygame
from center_indicator_sprite import CenterIndicator
from center_background_sprite import CenterBackground
from note_catcher_sprite import NoteCatcher
from note_lane_sprite import NoteLane   
from note_sprite import Note
from . import config_loader

class MapLoader():
    def __init__(self, screen:pygame.surface.Surface, dt):
        self.screen = screen

        # init of sprite groups
        self.center_group = pygame.sprite.GroupSingle(CenterIndicator(screen))

        self.note_catcher_group = pygame.sprite.Group()
        for side in ("left", "right", "top", "bottom"):
            self.note_catcher_group.add(NoteCatcher(side, self.center_group.sprite.rect))

        self.note_lane_group = pygame.sprite.Group()
        for sprite in self.note_catcher_group.sprites():
            self.note_lane_group.add(NoteLane(screen, sprite.type, sprite.rect))

        self.center_background_group = pygame.sprite.GroupSingle(CenterBackground([sprite for sprite in self.note_catcher_group.sprites()]))

        self.note_group = pygame.sprite.Group()
        song_config = config_loader.option_load("songs/Onoken - Sagashi Mono/sagashi_mono.nnb", True)
        if song_config is not None:
            for key, value in song_config["[NoteTimings]"].items():
                side = song_config["[NoteTimings]"][key]["side"]
                for sprite in self.note_catcher_group.sprites():
                    if sprite.type == side:
                        catcher = sprite.rect
                self.note_group.add(Note(dt= dt, screen= screen, catcher= catcher, **{f"{key}": value}))

    def set_delay(self):
        delay_start = pygame.time.get_ticks()
        # taking note sprite with id = 0 and checking it's start pos
        if(self.note_group.sprites[0].side in ("left", "right") and self.note_group.sprites[0].start_pos < 890):
            pass
        elif(self.note_group.sprites[0].side in ("top", "bottom") and self.note_group.sprites[0].start_pos < 470):
            pass

    def sprites_draw(self):
        # drawing sprite groups
        self.center_background_group.draw()
        
        # here is note draw
        self.center_group.draw()
        self.note_catcher_group.draw()
        self.note_lane_group.draw()

    def sprites_update(self, type, pressed):
        for sprite in self.note_catcher_group.sprites():
            if sprite.type == type:
                sprite.update(pressed)

    def song_play(self):
        pass

    def get_event(self, event):
        # ?????
        pass