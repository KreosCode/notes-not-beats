from pygame import font

class States(object):
    def __init__(self):
        self.done  = False      # is the trigger for a change of current state
        self.next = None        # indicates which state will be next (value is the key in state_dict in main.py)
        self.quit = False       # is the trigger for closing the *entire* program
        self.previous = None    # refers to the previous state (value is the key in state_dict in main.py) if current one not the first
        self.font = font.Font("src/fonts/metropolis.thin.otf", 48)