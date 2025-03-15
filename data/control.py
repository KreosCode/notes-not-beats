import pygame

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size, self.flags)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Notes Not Beat")

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        
    def flip_state(self, dt):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(dt)
        self.state.previous = previous

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state(dt)
        self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)
            
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()