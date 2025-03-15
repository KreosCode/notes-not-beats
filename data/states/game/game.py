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
        self.time_get = False # help to take current time only one time
        self.game_state = False # state of main game (gameplay)
        self.bg_get = False # help to get bg sizes only one time

        # sprites
        self.center_indicator = None # referring to group single
        self.note_lane = None # referring to group single
        self.note_catcher_sprites = pygame.sprite.Group() # referring to sprites group
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
        self.song_config = None

        # sprite clear (rewrite it to separate func)
        self.center_indicator = None
        self.sprites_assigned = False
        self.note_catcher_sprites.empty()

        pygame.mouse.set_visible(True)

    def startup(self):
        pygame.mouse.set_visible(False)

        self.song_config = config_loader.option_load("songs/Onoken - Sagashi Mono/sagashi_mono.nnb", True)
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
                screen.blits([(self.bg_horizontal_surf, self.bg_horizontal_coords), (self.bg_vertical_surf, self.bg_vertical_coords)])

    def sprite_assign(self, screen):
        if not self.sprites_assigned:

            if self.center_indicator is None:

                self.center_indicator = pygame.sprite.GroupSingle(CenterIndicator(screen))

                if len(self.note_catcher_sprites.sprites()) != 4:
                    center_params = {
                        "center_midleft": self.center_indicator.sprite.rect.midleft,
                        "center_midright": self.center_indicator.sprite.rect.midright,
                        "center_midtop": self.center_indicator.sprite.rect.midtop,
                        "center_midbottom": self.center_indicator.sprite.rect.midbottom
                    }

                    self.note_catcher_sprites.add(NoteCatcher("left", **center_params), 
                                          NoteCatcher("right", **center_params),
                                          NoteCatcher("top", **center_params),
                                          NoteCatcher("bottom", **center_params))
        


                    # # for bg draw
                    # self.note_catcher_sprites_size = (note_catcher_sides["right"].rect.centerx - note_catcher_sides["left"].rect.centerx,
                    #                                   note_catcher_sides["bottom"].rect.centery - note_catcher_sides["top"].rect.centery)
                    # self.blit_coords = (note_catcher_sides["left"].rect.centerx, note_catcher_sides["top"].rect.centery)

            if self.note_lane is None:
                self.note_lane = pygame.sprite.GroupSingle(NoteLane(screen))

            self.sprites_assigned = True
    
    def sprite_draw(self, screen, dt):
        if self.sprites_assigned:
            self.note_lane.draw(screen)
            self.sprite_bg(screen)
            self.center_indicator.draw(screen)
            self.note_catcher_sprites.draw(screen)
        else:
            self.sprite_assign(screen)

    def main_game_draw(self, screen, dt):
        self.sprite_draw(screen, dt)

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

        if self.countdown_started:
            self.countdown(screen, pygame.time.get_ticks() / 1000)
        