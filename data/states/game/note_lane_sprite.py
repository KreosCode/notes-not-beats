# important thing:
# all note lanes have the
# same length to simplify
# note spawn logic
# currently: length = vertical lane length

import pygame

class NoteLane(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface):
        super().__init__()
        # lane_sprite is vertical line (for details see it directly)
        lane_sprite = pygame.image.load("src/sprites/note_lane.png").convert_alpha()
        lane_sprite_vertical = pygame.transform.scale(lane_sprite, (lane_sprite.get_width(), screen.get_height()))
        lane_sprite_horizontal = pygame.transform.rotate(lane_sprite_vertical, 90)
        # same length => square Surface
        lanes_surf = pygame.Surface((lane_sprite_horizontal.get_width(),
                                     lane_sprite_vertical.get_height()))
        # bliting vertical and horizontal lanes at once respectively
        lanes_surf.blits(blit_sequence=((lane_sprite_vertical, (lanes_surf.get_width()/2 - lane_sprite_vertical.get_width()/2, 0)),
                                        (lane_sprite_horizontal, (0, lanes_surf.get_height()/2 - lane_sprite_horizontal.get_height()/2))))
        # making background invisible
        lanes_surf.set_colorkey((0, 0, 0))
        self.image = lanes_surf
        self.rect = self.image.get_rect(center= (screen.get_width()/2, screen.get_height()/2))

        # match catcher_type:
        #     case "left":
        #         lane_length = catcher_rect.centerx
        #         self.image = pygame.transform.rotate(self.image, 90)
        #         self.image = pygame.transform.scale(self.image, (lane_length, self.image.get_height()))
        #         self.rect = self.image.get_rect(midleft = (0, catcher_rect.centery))
        #     case "right":
        #         lane_length = screen.get_width() - catcher_rect.centerx
        #         self.image = pygame.transform.rotate(self.image, 90)
        #         self.image = pygame.transform.scale(self.image, (lane_length, self.image.get_height()))
        #         self.rect = self.image.get_rect(midright = (screen.get_width(), catcher_rect.centery))
        #     case "top":
        #         lane_length = catcher_rect.centery
        #         self.image = pygame.transform.scale(self.image, (self.image.get_width(), lane_length))
        #         self.rect = self.image.get_rect(midtop = (catcher_rect.centerx, 0))
        #     case "bottom":
        #         lane_length = screen.get_height() - catcher_rect.centery
        #         self.image = pygame.transform.scale(self.image, (self.image.get_width(), lane_length))
        #         self.rect = self.image.get_rect(midbottom = (catcher_rect.centerx, screen.get_height()))
        

    def update(self):
        pass