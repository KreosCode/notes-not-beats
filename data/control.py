# 'Control' class controls entire program
# which include switching between the 
# states

# Control does not have to be a class
# but to keep all things in the same
# order and avoid code bloat we contain
# one in the class as a separate module

import pygame

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size, self.flags)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.caption)

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        
    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    # this is the ONLY *event* loop
    # in the entire program
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)
    
    # Whole game is constantly just
    # looping main_game_loop()

    # this is the ONLY *game* loop
    # in the entire program
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()