import pygame

import settings


class Button:
    """Button used in the CPS Test"""
    def __init__(self, window: pygame.surface.Surface,  args, text='',command=None):
        self.window = window
        self.command = command
        self.args = args

        self.button_size = settings.button_size
        self.color = pygame.Color(settings.button_color)
        font = pygame.font.SysFont('Consolas', 18)
        self.font_img = font.render(text, True, settings.text_color, self.color)

        self.rect_h = pygame.draw.rect(self.window, color=self.color, rect=(
            0,  # distance between button to the screen edge
            settings.bg_size[1] - settings.button_size[1],
            settings.button_size[0],  # the size of the button
            settings.button_size[1]
        )).h

    def draw(self):
        pygame.draw.rect(self.window, color=self.color, rect=(
            0,  # distance between button to the screen edge
            settings.bg_size[1] - settings.button_size[1],
            settings.button_size[0],  # the size of the button
            settings.button_size[1]
        ))
        self.window.blit(self.font_img, (
            0.5*self.button_size[0] - 0.5*self.font_img.get_width(),
            settings.bg_size[1] - settings.button_size[1] + 0.5*self.rect_h - 0.5*self.font_img.get_height(),
        ))

    def update(self, pos):
        if settings.button_size[0] >= pos[0] and settings.bg_size[1] >= pos[1] >= (settings.bg_size[1] -
                                                                                   settings.button_size[1]):
            self.command(self.args[0])
