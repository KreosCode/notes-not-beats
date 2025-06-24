import pygame
# from ...state import States

class NAME(States):
    def __init__(self):
        super().__init__()

        self.next = "*name of the next state*"

    def startup(self):
        pass

    def cleanup(self):
        pass

    def get_event(self, event):
        if pygame.event == event:
            

    def draw(self, screen):
        screen.fill("#000000")

    def update(self, screen, dt):
        self.draw(screen)