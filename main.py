import pygame
from sys import exit
# 'State' may be some window(splash screen, result screen), menu(pause) etc
# from data.state import States
from data.control import Control
"""CHANGE IT"""
from data.states.menu.menu import Menu # should found a way to import state only if needed
from data.states.game.game import Game
"""_________"""

pygame.init()

"""MAKE THIS TO BE READEN FROM .ini FILE OR SOME SHIT"""
# general settings
settings = {    
    "size": (1920, 1080),
    "fps": 60,
    "flags": pygame.FULLSCREEN,
    "caption": "Notes Not Beat"
}

# dict of game states
state_dict = {
    "menu": Menu(),
    "game": Game()
}
"""__________________________________________________"""

app = Control(**settings)
app.setup_states(state_dict, "menu")
app.main_game_loop()

pygame.quit()
exit()