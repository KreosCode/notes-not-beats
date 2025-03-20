import pygame
from ...state import States
from .center_indicator_sprite import CenterIndicator
from .note_catcher_sprite import NoteCatcher
from .note_lane_sprite import NoteLane
from .note_sprite import Note
from . import config_loader

class Game(States):
    def __init__(self):
        super().__init__()
        self.next = "menu"

        self.countdown_time = 0 # seconds needed to start the main game
        self.bg_color = "#010203" # bg color

        self.countdown_started = False #  state of countdown
        self.time_get = False # help to take current time only one time (need for countdown)
        self.game_state = False # state of main game (gameplay)
        self.bg_get = False # help to get bg sizes only one time
        self.song_started = False # help to start song only one time

        # sprites
        self.center_indicator = None # referring to group single
        self.note_lane = None # referring to group single
        self.note_catcher_sprites = pygame.sprite.Group() # referring to sprites group
        self.note_sprites = pygame.sprite.Group() # referring to sprites group
        self.sprites_assigned = False # show if sprites assigned

        # keybinginds
        self.keybinds = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "top": pygame.K_w,
            "bottom": pygame.K_s
        }

    def cleanup(self):
        # variable reset
        self.countdown_started = False
        self.time_get = False
        self.game_state = False
        self.bg_get = False

        # sprite clear (rewrite it to separate func)
        self.center_indicator = None
        self.sprites_assigned = False
        self.note_catcher_sprites.empty()
        self.note_sprites.empty()

        # SUBJECT TO CHANGE
        self.song_started = False
        self.song.stop()
        
        pygame.mouse.set_visible(True)

    def startup(self):
        pygame.mouse.set_visible(False)
        self.countdown_started = True

    def bg_assign(self):
        if not self.bg_get:
            note_catcher_sides = {
                "left": None, 
                "right": None,
                "top": None,
                "bottom": None
            }
            for i in note_catcher_sides.keys():
                for x in self.note_catcher_sprites.sprites():
                    if x.type == i:
                        note_catcher_sides[i] = x

            """Maybe make bg sprites"""
            bg_horizontal_size = (note_catcher_sides["right"].rect.left - note_catcher_sides["left"].rect.right,
                                  self.center_indicator.sprite.rect.bottom - self.center_indicator.sprite.rect.top)
            self.bg_horizontal_coords = (note_catcher_sides["left"].rect.right, self.center_indicator.sprite.rect.top)
            self.bg_horizontal_surf = pygame.Surface(bg_horizontal_size)

            bg_vertical_size = (self.center_indicator.sprite.rect.right - self.center_indicator.sprite.rect.left,
                                note_catcher_sides["bottom"].rect.top - note_catcher_sides["top"].rect.bottom)
            self.bg_vertical_coords = (self.center_indicator.sprite.rect.left, note_catcher_sides["top"].rect.bottom)
            self.bg_vertical_surf = pygame.Surface(bg_vertical_size)
            """______________________"""

            self.bg_get = True

    def sprite_bg(self, screen):
        if not self.bg_get:
            self.bg_assign()
        else:
            if self.sprites_assigned:
                pass

    def sprite_assign(self, screen, dt):
        if not self.sprites_assigned: 
            # catchers + center
            if self.center_indicator is None:

                self.center_indicator = pygame.sprite.GroupSingle(CenterIndicator(screen))

                if len(self.note_catcher_sprites.sprites()) != 4:
                    center_rect = self.center_indicator.sprite.rect

                    self.note_catcher_sprites.add(NoteCatcher("left", center_rect), 
                                          NoteCatcher("right", center_rect),
                                          NoteCatcher("top", center_rect),
                                          NoteCatcher("bottom", center_rect))
            # note lane
            if self.note_lane is None:
                self.note_lane = pygame.sprite.Group()
                for sprite in self.note_catcher_sprites.sprites():
                    print(sprite.type)
                    self.note_lane.add(NoteLane(screen, sprite.type, sprite.rect))
            # notes
            if not self.note_sprites.sprites():
                song_config = config_loader.option_load("songs/Onoken - Sagashi Mono/sagashi_mono.nnb", True)
                if song_config is not None:
                    for key, value in song_config["[NoteTimings]"].items():
                        side = song_config["[NoteTimings]"][key]["side"]
                        for sprite in self.note_catcher_sprites.sprites():
                            if sprite.type == side:
                                catcher = sprite.rect
                        self.note_sprites.add(Note(dt, screen, catcher, **{f"{key}": value}))
                else: 
                    print("error, no note timings provided")

            self.sprites_assigned = True
    
    def sprite_draw(self, screen, dt):
        if self.sprites_assigned:
            self.note_lane.draw(screen)
            self.sprite_bg(screen)
            self.center_indicator.draw(screen)
            self.note_sprites.draw(screen)
            self.note_catcher_sprites.draw(screen)
        else:
            self.sprite_assign(screen, dt)

    def play_song(self):
        if not self.song_started:
            self.song = pygame.mixer.Sound("songs/Onoken - Sagashi Mono/sagashi_mono.mp3")
            self.song.set_volume(0.2)
            self.song.play()
            self.song_started = True

    def main_game_draw(self, screen, dt):
        self.sprite_draw(screen, dt)
        self.play_song()

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            """ just for testing. need to be rewritten """
            if event.key == pygame.K_SPACE:
                self.done = True
            """_______________________________________"""
        if self.game_state and self.sprites_assigned:

            if event.type == pygame.KEYDOWN:
                # use keydown_time for know keypressed timing
                keydown_time = pygame.time.get_ticks() / 1000
                for keytype, keybind in self.keybinds.items():
                    if event.key == keybind:
                        for i in self.note_catcher_sprites.sprites():
                            if i.type == keytype:
                                i.update(pressed = True)
            
            if event.type == pygame.KEYUP:
                # use keydown_time for know keypressed timing
                keydown_time = pygame.time.get_ticks() / 1000
                for keytype, keybind in self.keybinds.items():
                    if event.key == keybind:
                        for i in self.note_catcher_sprites.sprites():
                            if i.type == keytype:
                                i.update(pressed = False)
                    
    def countdown(self, screen, current_time):
        if not self.time_get:
            self.start_time = current_time
            self.time_get = True
        
        if self.countdown_time - int(current_time - self.start_time) > 0:
            time_surf = self.font.render(f"{self.countdown_time - int(current_time - self.start_time)}", True, "#ffffff")
            screen.blit(time_surf, (screen.get_width() / 2 - time_surf.get_width() / 2, screen.get_height() / 2 - time_surf.get_height() / 2))
        else:
            self.countdown_started = False
            self.time_get = False
            self.game_state = True

    def draw(self, screen):
            screen.fill(self.bg_color)

    def update(self, screen, dt):
        self.draw(screen)
        
        if self.game_state:
            self.main_game_draw(screen, dt)
            self.note_sprites.update()
            # TEMPORARY
            pygame.sprite.groupcollide(self.note_sprites, self.center_indicator, dokilla = True, dokillb = False)
            # TEMPORARY

        if self.countdown_started:
            self.countdown(screen, pygame.time.get_ticks() / 1000)
        