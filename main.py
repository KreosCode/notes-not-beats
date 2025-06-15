import pygame
from sys import exit
# 'State' may be some window(splash screen, result screen), menu(pause) etc
# from data.state import States
from data.control import Control
from data.states.menu.menu import Menu
from data.states.game.game import Game

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
app.setup_states(state_dict=state_dict, start_state="menu")
app.main_game_loop()

pygame.quit()
exit()