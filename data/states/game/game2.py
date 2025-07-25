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
from .sprites.debug_info_sprite import DebugInfo
from . import config_loader

class Game2(States):
    def __init__(self):
        super().__init__()
        self.next = "menu"

        self.bg_color = "#010203"
        self.sprite_assigned = False                   # indicates if sprite_assign() is executed

        # game constants
        self.APPROACH_TIME = 2000                      # time notes are visible before hitting (ms)
        self.DISTANCE = 440                            # distance between screen edge and catcher (same for all sides)
        self.REMOVE_DELAY = 200                        # time after hit to remove note (ms)

        # hit detect settings
        self.HIT_WINDOW_PERFECT = 50    # +- 50ms for perfect
        self.HIT_WINDOW_GOOD = 100      # +- 100ms for good
        self.HIT_WINDOW_OK = 150        # += 150ms for ok
        self.HIT_WINDOW_MISS = 200      # += 200ms for miss

        self.keybinds = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "top": pygame.K_w,
            "bottom": pygame.K_s
        }

        # for sound tracking
        self.side_current_sound = {
            "left": None,
            "right": None,
            "top": None,
            "bottom": None
        }
        # if side doesn't have any notes/sounds
        self.default_sound = None

    def startup(self):
        self.score = 0
        self.current_combo = 0
        self.max_combo = 0
        self.scores_count = {
            "PERFECT": 0,
            "GOOD": 0,
            "OK": 0,
            "MISS": 0
        }

        # vvv Temporary part (parsing)
        path = "songs/Onoken - Sagashi Mono/sagashi_mono.nnb"
        self.song_general_info = config_loader.option_load(path, False)["[General]"]
        # self.song_difficulty_info = config_loader.option_load("songs/Onoken - Sagashi Mono/sagashi_mono.nnb", False)["[Difficulty]"]
        # self.song_timing_options_info = config_loader.option_load("songs/Onoken - Sagashi Mono/sagashi_mono.nnb", False)["[TimingOptions]"]
        self.song_note_timings = config_loader.option_load(path, True)["[NoteTimings]"]
        # ^^^ Temporary part (parsing)

        self.unspawned_notes = []       # for tracking unspawned notes
        self.prepare_note_data()

        delay = 0
        pygame.mixer.music.load(f"songs/Onoken - Sagashi Mono/{self.song_general_info['song_filename']}")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(start=delay)

        # vv temp
        songtemp = pygame.mixer.Sound(f"songs/Onoken - Sagashi Mono/{self.song_general_info['song_filename']}")
        self.song_length = songtemp.get_length()
        self.song_start_time = pygame.time.get_ticks()      # need to check current song progress
        self.song_started = True                            # indicates if song started

        self.default_sound = pygame.mixer.Sound(f"songs/Onoken - Sagashi Mono/soft-hitwhistle.wav")

        self.sound_cache = {}
        for _, sound_name in self.side_current_sound.items():
            if sound_name not in self.sound_cache:
                self.sound_cache[sound_name] = pygame.mixer.Sound(f"songs/Onoken - Sagashi Mono/{sound_name}")
                self.sound_cache[sound_name].set_volume(0.05)

    def prepare_note_data(self):
        for _, note_data in self.song_note_timings.items():
            self.unspawned_notes.append({
                'type': note_data['type'],
                'sound_name1': note_data['sound_name1'],
                'end_timing1': note_data['end_timing1'],
                'side': note_data['side']
            })
        
        # Sort by timing
        self.unspawned_notes.sort(key=lambda x: x['end_timing1'])

        # temp dict for first side notes tracking
        first_notes = {side: None for side in self.keybinds.keys()}

        # find first note occurance for each side
        for note_data in self.unspawned_notes:
            side = note_data["side"]
            if first_notes[side] is None or note_data['end_timing1'] < first_notes[side]['end_timing1']:
                first_notes[side] = note_data
            else:
                self.side_current_sound[side] = "soft-hitwhistle.wav"

        # setting current sounds for each side
        for side, note_data in first_notes.items():
            if note_data:
                self.side_current_sound[side] = note_data['sound_name1']
            else:
                self.side_current_sound[side] = "soft-hitwhistle.wav" 

    def cleanup(self):
        # 'unpressing' all indicators
        for sprite in self.key_indicators.sprites():
            sprite.update(pressed = False)
        pygame.mixer.music.stop()
        self.unspawned_notes.clear()
        self.notes.empty()
        self.sprite_assigned = False
        self.song_started = False

        # transfering all combo, acc results to the file in 'states' folder
        with open("data/states/result/result.txt", encoding="utf-8", mode="w") as f:
            for key, value in self.scores_count.items():
                f.write(f"{key}: {value}\n")
            f.write(f"score: {self.score}\n")
            f.write(f"max_combo: {self.max_combo}\n")

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
           # return to menu
           if event.key == pygame.K_SPACE:
               self.next = "menu"
               self.done = True

           # skip song and show results
           if self.song_started:
               if event.key == pygame.K_n:
                   self.next = "result"
                   self.done = True

           # changing key_indicator sprite if
           # corresponding key is being pressed
           for action, keybind in self.keybinds.items():
                if event.key == keybind:
                    for sprite in self.key_indicators.sprites():
                        if sprite.side == action:
                            sprite.update(pressed = True)
                        
                    self.play_sound_for_side(action)

                    if self.song_started:
                        self.check_hit_for_side(action)

        if event.type == pygame.KEYUP:
           # changing key_indicator sprite if
           # corresponding key is being unpressed
           for action, keybind in self.keybinds.items():
                if event.key == keybind:
                    for sprite in self.key_indicators.sprites():
                        if sprite.side == action:
                            sprite.update(pressed = False)

    def play_sound_for_side(self, side):
        # playing sound for specific side
        sound_name = self.side_current_sound[side]
        
        if sound_name in self.sound_cache:
            self.sound_cache[sound_name].play()
        elif self.default_sound:
            self.default_sound.play()

    def check_hit_for_side(self, side):
        current_time = pygame.time.get_ticks() - self.song_start_time
        best_note = None        # closest to catcher note
        best_diff = 99999999
        hit_detected = False

        # finding the closest to the catcher note on current side
        for note in self.notes.sprites():
            if note.side == side:
                # time_diff can be negative value
                time_diff = current_time - note.end_timing1
                abs_diff = abs(time_diff)
                
                if abs_diff < best_diff:
                    best_note = note
                    best_diff = abs_diff
        
        # if note in the hit window
        if best_note and best_diff <= self.HIT_WINDOW_MISS:
            # accuracy based on timing
            if best_diff <= self.HIT_WINDOW_PERFECT:
                self.score += 300
                self.scores_count["PERFECT"] += 1
                hit_detected = True
            elif best_diff <= self.HIT_WINDOW_GOOD:
                self.score += 100
                self.scores_count["GOOD"] += 1
                hit_detected = True
            elif best_diff <= self.HIT_WINDOW_OK:
                self.score += 50
                self.scores_count["OK"] += 1
                hit_detected = True
            else:
                self.scores_count["MISS"] += 1
                self.current_combo = 0
        else:
            # if note skipped (no key pressed)
            self.scores_count["MISS"] += 1
            self.current_combo = 0
        
        # remove note if hit was successfull
        if hit_detected:
            best_note.kill()
            self.current_combo += 1
            self.max_combo = max(self.max_combo, self.current_combo)

    def update(self, screen, dt):
        screen.fill(self.bg_color)          # updating background

        if not self.sprite_assigned:        # assigning sprites to their groups
            self.sprite_assign(screen)
            self.sprite_assigned = True
        
        if self.song_started:
            self.current_time = pygame.time.get_ticks() - self.song_start_time
            self.spawn_notes(self.current_time)                                                    # spawn new notes
            self.update_notes(dt, self.current_time)                                               # update spawned notes

            self.update_side_sounds(self.current_time)

        self.debug.update(self.current_time)
        self.draw(screen)

    def update_side_sounds(self, current_time):
        # notes in future (unplayed notes)
        upcoming_notes = {side: [] for side in self.keybinds.keys()}

        for note in self.notes.sprites():
            if note.end_timing1 > current_time:
                upcoming_notes[note.side].append(note)
        
        for note_data in self.unspawned_notes:
            if note_data['end_timing1'] > current_time:
                upcoming_notes[note_data['side']].append(note_data)

        for side in self.keybinds.keys():
            notes = upcoming_notes[side]
            if notes:
                # sorting with end_timing1 key
                notes.sort(key=lambda x: x.end_timing1 if hasattr(x, 'end_timing1') else x['end_timing1'])
                # taking 1st note in list
                first_note = notes[0]
                sound_name = first_note.sound_name1 if hasattr(first_note, 'sound_name1') else first_note['sound_name1']
                # updating sound if it haven't changed
                if sound_name != self.side_current_sound[side]:
                    self.side_current_sound[side] = sound_name
                    # load sound, if one not in cache
                    if sound_name not in self.sound_cache:
                            self.sound_cache[sound_name] = pygame.mixer.Sound(f"songs/Onoken - Sagashi Mono/{sound_name}")
                            self.sound_cache[sound_name].set_volume(0.05)
                            
            else:
                # if no notes on side, load default sound
                if self.side_current_sound[side] != "soft-hitwhistle.wav":
                    self.side_current_sound[side] = "soft-hitwhistle.wav"

    def spawn_notes(self, current_time):
        # spawn notes at correct time
        while self.unspawned_notes:
            note_data = self.unspawned_notes[0]
            spawn_time = note_data['end_timing1'] - self.APPROACH_TIME

            if current_time >= spawn_time:
                new_note = Note(self.note_lane.sprite.rect, self.APPROACH_TIME, self.DISTANCE, spawn_time,
                                note_data["type"], note_data["sound_name1"], note_data["end_timing1"], note_data["side"])
                
                # if note spawns late
                if current_time > spawn_time:
                    time_passed = current_time - spawn_time
                    progress = min(1.0, time_passed / self.APPROACH_TIME)           # 1.0 - note pos=catcher pos, 0.0 - note pos = start pos

                    if new_note.side == "left":
                        new_note.rect.x += self.DISTANCE * progress
                    elif new_note.side == "right":
                        new_note.rect.x -= self.DISTANCE * progress
                    elif new_note.side == "top":
                        new_note.rect.y += self.DISTANCE * progress
                    elif new_note.side == "bottom":
                        new_note.rect.y -= self.DISTANCE * progress

                self.notes.add(new_note)
                self.unspawned_notes.pop(0)
            else:
                break

    def update_notes(self, dt, current_time):
        self.notes.update(dt)

        # removing expired notes from notes sprite group
        expired_notes = [note for note in self.notes.sprites() if current_time > note.end_timing1 + self.REMOVE_DELAY]
        for note in expired_notes:
            note.kill()


    def draw(self, screen):
        self.note_lane.draw(screen)
        self.notes.draw(screen)
        self.center_background.draw(screen)
        self.center_indicator.draw(screen)
        self.key_indicators.draw(screen)
        self.note_catcher.draw(screen)
        self.debug.draw(screen)

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
        self.notes = pygame.sprite.Group()

        self.debug = pygame.sprite.GroupSingle(DebugInfo(self.song_length))