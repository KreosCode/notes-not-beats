# show (notes pressed, accuracy, score)

import pygame
from ...state import States
from .sprites.text_sprite import Text

class Result(States):
    def __init__(self):
        super().__init__()

        self.next = "menu"

        self.sprite_assigned = False
        self.bg_color = "#010203"

    def startup(self):
        self.score_info = {}
        with open("data/states/result/result.txt", encoding="utf-8", mode="r") as f:
            for line in f.readlines():
                key_value = line.replace("\n", "").split(":")
                # converting to int error handle
                try:
                    self.score_info[key_value[0]] = int(key_value[1])
                except Exception as e:
                    self.score_info[key_value[0]] = None

    def cleanup(self):
        self.sprite_assigned = False

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.done = True

    def draw(self, screen):
        self.texts.draw(screen)

    def sprite_assign(self):
        self.texts = pygame.sprite.Group()
        self.texts.add(Text(f"score: {self.score_info["score"]}", 32, "#ffffff", (0, 0)))
        self.texts.add(Text(f"max_combo: {self.score_info["max_combo"]}", 32, "#ffffff", (0, 32 + 2)))
        self.texts.add(Text(f"PERFECT: {self.score_info["PERFECT"]}", 32, "#39f400", (0, 66 + 2)))
        self.texts.add(Text(f"GOOD: {self.score_info["GOOD"]}", 32, "#e4f307", (0, 100 + 2)))
        self.texts.add(Text(f"OK: {self.score_info["OK"]}", 32, "#f5a209", (0, 134 + 2)))
        self.texts.add(Text(f"MISS: {self.score_info["MISS"]}", 32, "#fb1e1e", (0, 168 + 2)))
        self.texts.add(Text(f"Press SPACE for menu screen", 32, "#ffffff", (0, 300)))

    def update(self, screen, dt):
        screen.fill(self.bg_color)

        if not self.sprite_assigned:
            self.sprite_assign()
            self.sprite_assigned = True

        self.draw(screen)