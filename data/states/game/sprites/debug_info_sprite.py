# debug sprite contains info about song
# song name, time passed from start
# progress etc

import pygame

# takes time in ms (e.g 16000) and convert it to MM:SS format (e.g 0:16)
def convert_to_MM_SS(time: int, type: str):
    match type:
        case 'ms':
            if int((time/1000)%60) < 10:
                return f"{int((time/1000)//60)}:0{int((time/1000)%60)}"
            else:
                return f"{int((time/1000)//60)}:{int((time/1000)%60)}"
        case 'sec':
            if int(time%60) < 10:
                return f"{int(time//60)}:0{int(time%60)}"
            else:
                return f"{int(time//60)}:{int(time%60)}"

class DebugInfo(pygame.sprite.Sprite):
    def __init__(self, song_length: float):
        super().__init__()
        font_size = 32
        self.song_length = song_length
        self.font = pygame.font.Font("src/fonts/metropolis.thin.otf", font_size)
        text = f"Progress - {convert_to_MM_SS(0, 'ms')}/{convert_to_MM_SS(self.song_length, 'sec')}"
        self.image = self.font.render(text, True, "#ffffff")
        self.rect = self.image.get_rect(topleft = (50, 50))


    def update(self, current_time: int):
        text = f"Progress - {convert_to_MM_SS(current_time, 'ms')}/{convert_to_MM_SS(self.song_length, 'sec')}"
        self.image = self.font.render(text, True, "#ffffff")