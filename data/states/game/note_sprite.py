import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, dt, screen: pygame.surface.Surface, catcher: pygame.rect.Rect, **timings):
        """
        types of timings kwargs:
        note - 1: {'type': 'single', 'sound_name1': 'soft-hitwhistle2.wav', 'end_timing1': '2660', 'side': 'top'}
        slider - 2: {'type': 'slider', 'sound_name1': 'soft-hitwhistle2.wav', 'sound_name2': 'pause', 'end_timing1': '3035', 'end_timing2': '3597', 'side': 'right'}
        """
        super().__init__()
        self.id = next(iter(timings))
        self.__dict__.update(timings[self.id])

        # IMPORTANT:
        # end_timing1 of next object has to be more then end_timing2 (if slider)/end_timing1 (if single)

        self.start_pos = (0, 0)
        self.pixel_per_frame = 2
        ms_per_frame = dt
        self.speed = self.pixel_per_frame/ms_per_frame
        
        # single note assign
        if self.type == "single":
            self.image = pygame.image.load("src/sprites/note.png").convert_alpha()
            if self.side == "left":
                self.start_pos = (-self.image.get_width() - self.end_timing1 * self.speed, 
                                  catcher.y)
            elif self.side == "right":
                self.start_pos = (screen.get_width() + self.image.get_width() + self.end_timing1 * self.speed, 
                                  catcher.y)
            elif self.side == "top":
                self.start_pos = (catcher.x, 
                                  -self.image.get_height() - self.end_timing1 * self.speed)
            elif self.side == "bottom":
                self.start_pos = (catcher.x, 
                                  screen.get_height() + self.image.get_height() + self.end_timing1 * self.speed)
                
            self.rect = self.image.get_rect(topleft = self.start_pos)

        elif self.type == "slider":
            slider_start = pygame.image.load("src/sprites/note.png").convert_alpha()
            slider_body = pygame.image.load("src/sprites/slider_body.png").convert_alpha()
            slider_head = pygame.image.load("src/sprites/slider_head.png").convert_alpha()

            if self.side in ("left", "right"):
                slider_body = pygame.transform.rotate(slider_body, 90).convert_alpha()
                slider_body_length = (self.end_timing2 - self.end_timing1) * self.speed - slider_head.get_height()
                slider_body = pygame.transform.scale(slider_body, (slider_head.get_height() + slider_body_length, slider_body.get_height())).convert_alpha()

                self.image = pygame.surface.Surface((slider_head.get_height() + slider_body.get_width() + slider_start.get_width() / 2,
                                                     slider_start.get_height())).convert_alpha()

                if self.side == "left":
                    slider_head = pygame.transform.rotate(slider_head, 90).convert_alpha()
                    self.image.blits(((slider_head, (0, 0)),
                                      (slider_body, (slider_head.get_width(), 0)),
                                      (slider_start, (slider_head.get_width() + slider_body.get_width() - slider_start.get_width() / 2, 0))))
                    self.start_pos = (-self.image.get_width() - self.end_timing1 * self.speed, 
                                      catcher.y)
                
                if self.side == "right":
                    slider_head = pygame.transform.rotate(slider_head, -90).convert_alpha()
                    self.image.blits(((slider_start, (0, 0)),
                                      (slider_body, (slider_start.get_width() / 2, 0)),
                                      (slider_head, (slider_start.get_width() / 2 + slider_body.get_width(), 0))))
                    self.start_pos = (screen.get_width() + self.image.get_width() + self.end_timing1 * self.speed, 
                                      catcher.y)
               
            elif self.side in ("top", "bottom"):
                slider_body_length = (self.end_timing2 - self.end_timing1) * self.speed - slider_head.get_height()
                slider_body = pygame.transform.scale(slider_body, (slider_body.get_width(), slider_body_length)).convert_alpha()

                self.image = pygame.surface.Surface((slider_start.get_width(), 
                                                     slider_head.get_height() + slider_body.get_height() + slider_start.get_height() / 2)).convert_alpha()

                if self.side == "top":
                    self.image.blits(((slider_head, (0, 0)),
                                      (slider_body, (0, slider_head.get_height())),
                                      (slider_start, (0, slider_head.get_height() + slider_body.get_height() - slider_start.get_height() / 2))))
                    self.start_pos = (catcher.x, 
                                 -self.image.get_height() - self.end_timing1 * self.speed)

                elif self.side == "bottom":
                    slider_head = pygame.transform.flip(slider_head, False, True).convert_alpha()
                    self.image.blits(((slider_start, (0, 0)),
                                     (slider_body, (0, slider_start.get_height() / 2)),
                                     (slider_head, (0, slider_start.get_height() / 2 + slider_body.get_height()))))
                    self.start_pos = (catcher.x, 
                                 screen.get_height() + self.image.get_height() + self.end_timing1 * self.speed)
                    
            self.rect = self.image.get_rect(topleft = self.start_pos)   

        
        
            
    def move(self):
        if self.side == "left":
            self.rect.x += self.pixel_per_frame
        if self.side == "right":
            self.rect.x -= self.pixel_per_frame
        if self.side == "top":
            self.rect.y += self.pixel_per_frame
        if self.side == "bottom":
            self.rect.y -= self.pixel_per_frame

    def update(self):
        self.move()