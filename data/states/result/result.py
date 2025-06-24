# show (notes pressed, accuracy, score)

import pygame
from ...state import States

class Result(States):
    def __init__(self):
        super().__init__()

        self.next = "menu"

    def startup(self):
        pass

    def cleanup(self):
        pass

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.done = True

    def draw(self, screen):
        screen.fill("#000000")

    def update(self, screen, dt):
        self.draw(screen)