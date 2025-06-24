import pygame

# need to be rewritten
class Button(pygame.sprite.Sprite):
    def __init__(self, pos, color, text, button_type):
        super().__init__()
        # essentials
        size = 48
        self.quit = False # changeeeeeeeeeeeeeeeeeeeee
        self.play = False
        self.color = color
        self.text = text
        self.type = button_type
        self.font = pygame.font.Font("src/fonts/metropolis.thin.otf", size)

        # audio
        self.audio_state = False # false - not played
        self.hover_sound = pygame.mixer.Sound("src/sounds/button_hover.mp3")
        self.clicked_sound = pygame.mixer.Sound("src/sounds/button_clicked.mp3")
        self.hover_sound.set_volume(.03)
        self.clicked_sound.set_volume(.05)

        self.sign_surf = self.font.render("> ", True, self.color)
        self.text_surf = self.font.render(self.text, True, self.color)
        self.button_surf = pygame.Surface(((self.sign_surf.get_width() + self.text_surf.get_width()), self.text_surf.get_height()))
        self.button_surf.blit(self.text_surf, (self.sign_surf.get_width(), 0))
        self.button_surf.set_colorkey("#000000")

        self.image = self.button_surf
        self.rect = self.image.get_rect(topleft = pos)

    def hover(self):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.font.render(f"> {self.text}", True, self.color)

                if not self.audio_state:
                    self.hover_sound.play()
                    self.audio_state = True
            else:
                self.image = self.button_surf
                self.audio_state = False

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.type == "quit":
                    self.quit = True
                elif self.type == "play":
                    self.play = True
                    self.clicked_sound.play()

    def update(self):
        self.hover()