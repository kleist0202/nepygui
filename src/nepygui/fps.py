import time
import pygame


class Fps:
    def __init__(self, font_size=20, x=0, y=0):
        self.font_size = font_size
        self.x = x
        self.y = y
        self.cSec, self.cFrame, self.FPS, self.delta = 0, 0, 0, 0
        self.fps_font = pygame.font.SysFont("dejavusansmono", font_size)

    def fps(self):
        if self.cSec == time.strftime("%S"):
            self.cFrame += 1
        else:
            self.FPS = self.cFrame
            self.cFrame = 0
            self.cSec = time.strftime("%S")
            if self.FPS > 0:
                self.delta = 1 / self.FPS

    def show_fps(self, window):
        fps_overlay = self.fps_font.render(str(self.FPS), True, (255, 255, 0))
        window.blit(fps_overlay, (self.x, self.y))
