import sys
import json
import pygame

import settings
from button import Button
from timer import Timer

__author__ = ['LanlanMC']
__version__ = '1.2'

ctrl = r = False


class Test:
    """CPS Test using pygame"""

    def __init__(self, screen):
        """Initialize the test"""
        self.string = None

        # fonts
        self.score_font = pygame.font.SysFont('Consolas', 48)
        self.cps_font = pygame.font.SysFont('Consolas', 24)
        self.time_font = pygame.font.SysFont('Arial', 22)
        self.fps_font = pygame.font.SysFont('Consolas', 12)
        self.cps_best_font = pygame.font.SysFont('Consolas', 18)

        self.time = None  # timer
        self.cps = '0'
        self.cps_best = self.load()['cps_best']  # best score you've got
        self.score = 0  # clicked times

        self.started = False  # is the test started

        # pygame window
        pygame.display.set_caption('CPS Test')
        icon = pygame.font.SysFont('Arial', 64).render('CPS', True, (0, 200, 0))
        pygame.display.set_icon(icon)
        self.screen = screen

        self.click_area = pygame.draw.rect(self.screen, settings.click_area_color, (settings.bg_size[0] // 2,
                                                                                    0,
                                                                                    settings.click_area_size[0],
                                                                                    settings.click_area_size[1]))
        self.screen_rect = self.screen.get_rect()

        # show fps
        self.clock = pygame.time.Clock()
        self.fps = '0'

        self.button = Button(window=window, text='Retry', command=self.__init__, args=[self.screen])

    def save(self):
        """save the score"""
        with open('data', mode='w', encoding='UTF-8') as f:
            json.dump({'cps_best': self.cps_best}, f)

    @staticmethod
    def load():
        """load score from storage"""
        try:
            with open('data', mode='r', encoding='UTF-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return {'cps_best': 0}
        except EOFError:
            return {'cps_best': 0}
        except IOError:
            return {'cps_best': 0}
        except json.decoder.JSONDecodeError:
            return {'cps_best': 0}

    def check_best_score(self):
        """Check the best score"""
        if float(self.cps.replace('CPS: ', '')) >= self.cps_best:
            self.cps_best = float(self.cps.replace('CPS: ', ''))

    def _check_keys(self):
        global ctrl, r
        """Check the keys"""
        for event in pygame.event.get():
            # check quit
            if event.type == pygame.MOUSEBUTTONUP:
                # check mouse clicks
                pos = pygame.mouse.get_pos()
                self.button.update(pos)
                if 120 <= pos[0] <= 600:
                    if self.click_area[1] <= pos[1] <= (self.click_area[1] + self.click_area.h):
                        if not self.started:  # start the test
                            self.time = Timer()
                            self.started = True
                        self.score += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save()
                    sys.exit(0)
                elif event.key == pygame.K_r:
                    r = True
                elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    ctrl = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    r = False
                elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    ctrl = False

            elif event.type == pygame.QUIT:
                self.save()
                sys.exit(0)
        if ctrl and r:
            self.__init__(self.screen)

    def _check_keys_after(self, event):
        global ctrl, r
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                r = True
            elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                ctrl = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                r = False
            elif event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                ctrl = False

        if ctrl and r:
            self.__init__(self.screen)

    def _render(self):
        """Render font, click area and other things."""
        self.screen.fill((240, 240, 240))  # The background
        pygame.draw.rect(self.screen, (0, 116, 0),
                         (settings.bg_size[0] // 2 - settings.click_area_size[0] // 2,
                          0,
                          settings.click_area_size[0],
                          settings.click_area_size[1]))  # Click Area

        # get images ready
        if self.started:
            score_font_img = self.score_font.render(str(self.score), True, (255, 255, 255))
        else:
            score_font_img = pygame.font.SysFont('Arial', 22).render('Click the green area as fast as you can.', True,
                                                                     (255, 255, 255))
        cps_font_img = self.cps_font.render(self.string, True, (0, 0, 0))
        fps_img = self.fps_font.render(self.fps, True, (0, 0, 0))
        cps_best_img = self.cps_best_font.render('Best CPS: ' + str(self.cps_best), True, (0, 0, 0))

        # render the images
        self.screen.blit(cps_font_img, (self.screen_rect.w // 2 - cps_font_img.get_width() // 2,
                                        self.screen_rect.h * 0.75 - cps_font_img.get_height() // 2))
        self.screen.blit(score_font_img, (self.screen_rect.w // 2 - score_font_img.get_width() // 2,
                                          self.click_area.center[1] - score_font_img.get_height() // 2))  # Score
        self.screen.blit(fps_img, (0, 0))
        self.screen.blit(cps_best_img, (
            self.screen_rect.w - cps_best_img.get_width(), self.screen_rect.h - cps_best_img.get_height()))
        self.button.draw()

    def main(self):
        while True:
            if self.time is not None:  # show the cps
                try:
                    self.cps = 'CPS: ' + str(self.score / self.time.get_time())
                except ZeroDivisionError:
                    pass

                if self.time.is_end():  # time's up
                    self.cps = str(self.score / 10)
                    self.string = f"{self.cps[:self.cps.find('.') + 2]}  Time: 10"

            if self.time is None or not self.time.is_end():  # the test is not end
                self._check_keys()
                if hasattr(self.time, 'get_time'):
                    self.string = f"{self.cps[:self.cps.find('.') + 2]}  Time: {str(self.time.get_time())[:3]}"
                else:
                    self.string = ''
            else:  # not in testing
                self.check_best_score()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                        pygame.quit()
                        self.save()
                        break
                    self._check_keys_after(event)

            self._render()
            pygame.display.flip()

            # fps
            self.clock.tick(360)
            self.fps = 'fps: ' + str(int(self.clock.get_fps())) + '/360'


if __name__ == '__main__':
    pygame.init()

    window = pygame.display.set_mode(settings.bg_size)
    test = Test(screen=window)
    test.main()
