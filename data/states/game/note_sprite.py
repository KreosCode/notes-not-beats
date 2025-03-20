import pygame

class Note(pygame.sprite.Sprite):
    def __init__(self, dt, screen: pygame.surface.Surface, catcher: pygame.rect.Rect, **timings):
        """
        types of timings kwargs:
        note) 1: {'type': 'single', 'sound_name1': 'soft-hitwhistle2.wav', 'end_timing1': '2660', 'side': 'top'}
        slider) 2: {'type': 'slider', 'sound_name1': 'soft-hitwhistle2.wav', 'sound_name2': 'pause', 'end_timing1': '3035', 'end_timing2': '3597', 'side': 'right'}
        """
        super().__init__()
        self.id = next(iter(timings))
        self.__dict__.update(timings[self.id])

        self.speed_distance = 2 # subject to change
        speed = self.speed_distance / dt 
        length = catcher.centerx

        if self.type == "single":
            self.image = pygame.image.load("src/sprites/note.png").convert_alpha()

            start_timing = length / speed + self.end_timing1
            pos_adjust = start_timing * speed

            if self.side == "left":
                starter_pos = (-(self.image.get_width() + pos_adjust), catcher.y) # all starter_pos are refering to top-left
            elif self.side == "right":
                starter_pos = (screen.get_width() + pos_adjust, catcher.y)
            elif self.side == "top":
                starter_pos = (catcher.x, -(self.image.get_height() + pos_adjust))
            elif self.side == "bottom":
                starter_pos = (catcher.x, screen.get_height() + pos_adjust)

            self.rect = self.image.get_rect(topleft = starter_pos)

        elif self.type == "slider":
            slider_start_image = pygame.image.load("src/sprites/note.png").convert_alpha()
            slider_body_image = pygame.image.load("src/sprites/slider_body.png").convert_alpha()
            slider_head_image = pygame.image.load("src/sprites/slider_head.png").convert_alpha()
            length_multiplier = 1.2
            """
            slider body length [px] = (end_timing2 - end_timing1) * speed * length_multiplier
            
            (end_timing2 - end_timing1) - total time of the slider, ms
            speed - pixels per time in frame, px/ms
            length_multiplier - value to fix slider length
            """
            slider_body_length = int((self.end_timing2 - self.end_timing1) * speed * length_multiplier) # important value

            start_timing = length / speed + self.end_timing2
            pos_adjust = start_timing * speed

            if self.side in ("left", "right"):
                slider_body_image = pygame.transform.rotate(slider_body_image, 90)
                slider_body_image = pygame.transform.scale(slider_body_image, (slider_body_length, slider_body_image.get_height()))
                self.image = pygame.surface.Surface(size=(slider_head_image.get_width() + slider_body_image.get_width() + slider_start_image.get_width() / 2, catcher.height))

                # slider blit order: head=body -> start
                if self.side == "left":
                    slider_head_image = pygame.transform.rotate(slider_head_image, 90)
                    self.image.blits(blit_sequence= [(slider_head_image, (0, 0)),
                                                     (slider_body_image, (slider_head_image.get_width(), 0)),
                                                     (slider_start_image, (slider_head_image.get_width() + slider_body_image.get_width() - slider_start_image.get_width() / 2))])
                    starter_pos = (-(self.image.get_width() + pos_adjust), catcher.y)
                
                elif self.side == "right":
                    slider_head_image = pygame.transform.rotate(slider_head_image, -90)
                    self.image.blits(blit_sequence= [(slider_head_image, (slider_start_image.get_width() / 2 + slider_body_image.get_width(), 0)),
                                                     (slider_body_image, (slider_start_image.get_width() / 2, 0)),
                                                     (slider_start_image, (0, 0))])
                    starter_pos = (screen.get_width() + pos_adjust, catcher.y)
            
            elif self.side in ("top", "bottom"):
                slider_body_image = pygame.transform.scale(slider_body_image, (slider_body_image.get_width(), slider_body_length))
                self.image = pygame.surface.Surface(size=(catcher.width, slider_head_image.get_height() + slider_body_image.get_height() + slider_start_image.get_height() / 2))

                if self.side == "top":
                    self.image.blits(blit_sequence= [(slider_head_image, (0, 0)),
                                                     (slider_body_image, (0, slider_head_image.get_height())),
                                                     (slider_start_image, (0, slider_head_image.get_height() + slider_body_image.get_height() - slider_start_image.get_height() / 2))])
                    starter_pos = (catcher.x, -(self.image.get_height() + pos_adjust))
                
                elif self.side == "bottom":
                    slider_head_image = pygame.transform.flip(slider_head_image, False, True)
                    self.image.blits(blit_sequence= [(slider_head_image, (0, slider_start_image.get_height() / 2 + slider_body_image.get_height())),
                                                     (slider_body_image, (0, slider_start_image.get_height() / 2)),
                                                     (slider_start_image, (0, 0))])
                    starter_pos = (catcher.x, (screen.get_height() + pos_adjust))

            self.rect = self.image.get_rect(topleft = starter_pos)
        
    def move(self):
        match self.side:
            case "left":
                self.rect.right += self.speed_distance
            case "right":
                self.rect.left -= self.speed_distance
            case "top":
                self.rect.bottom += self.speed_distance
            case "bottom":
                self.rect.top -= self.speed_distance
    
    def update(self):
        self.move()