import pygame
from ...state import States
from .button import Button

class Menu(States):
    def __init__(self):
        super().__init__()

        self.next = "game"
        self.button_group = pygame.sprite.Group()
        self.button_group.add(Button((100, 500), "#ffffff", "Play", "play"), Button((100, 575), "#ffffff", "Quit", "quit"))
        # here and after:
        # because entire program is
        # running from the main.py
        # file, all the paths should
        # be set from main.py dir
        self.background_music = pygame.mixer.Sound("src/bg_music/bgm.mp3")
        self.background_music.set_volume(.02)
    def cleanup(self):
        self.background_music.stop()

    def startup(self):
        self.background_music.play()

    def get_event(self, event):
        for sprite in self.button_group.sprites():
            sprite.get_event(event)

    def button_state_check(self):
        for sprite in self.button_group.sprites():
            if sprite.quit == True:
                sprite.quit = False
                self.quit = True
            elif sprite.play == True:
                self.done = True
                sprite.play = False

    def draw(self, screen):
        screen.fill("#0D1321")
        self.button_group.draw(screen)
        self.button_group.update()

    def update(self, screen, dt):
        self.button_state_check()
        self.draw(screen)