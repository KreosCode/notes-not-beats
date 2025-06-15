from pygame import font

class States(object):
    def __init__(self):
        self.done  = False
        self.next = None
        self.quit = False
        self.previous = None
        self.font = font.Font("src/fonts/metropolis.thin.otf", 48)