import pygame
from .fps import Fps
from .widgets import Frame

class Window:
    def __init__(self, **args):

        # init pygame
        pygame.init()

        # variables

        self.fullscreen = False
        self.options = pygame.HWSURFACE | pygame.DOUBLEBUF

        self.screen = None
        self.running = True
        self.screen_color = (100, 100, 200)
        self.caption = "Project"
        self.resizable = True
        self.info = pygame.display.Info()
        self.window_size = (800, 600)

        self.widgets = []
        self.surfaces = []
        self.layouts = []

        self.clock = pygame.time.Clock()
        self.fps = Fps()

        self.delta_time = 0
        self.mouse_button = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()

        self.last_frame_time = pygame.time.get_ticks()

    def init_window(self):
        pygame.display.set_caption(self.caption)

        if self.fullscreen:
            self.window_size = (0, 0)
            self.options |= pygame.FULLSCREEN

        if self.resizable:
            self.options |= pygame.RESIZABLE

        self.screen = pygame.display.set_mode(self.window_size, self.options)
        
        for layout in self.layouts:
            layout.put()

    def set_fullscreen(self, fullscreen: bool) -> None:
        self.fullscreen = fullscreen

    def set_screen_color(self, r: int, g: int, b: int) -> None:
        self.screen_color = (r, g, b)

    def set_caption(self, caption: str) -> None:
        self.caption = caption

    def set_window_size(self, w: int, h: int) -> None:
        self.window_size = (w, h)

    def get_screen(self):
        return self.screen

    def get_size(self):
        return self.window_size

    def main_loop(self) -> None:
        while self.running:
            event_list = pygame.event.get()
            self.window_size = self.screen.get_size()
            self.global_events(event_list)
            self.screen.fill(self.screen_color)

            # ------------ scene ------------- #

            # get mouse and keyboard input
            self.mouse_button = pygame.mouse.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            self.keys = pygame.key.get_pressed()

            for widget in self.widgets:
                widget.draw(self.screen, self.mouse_pos, self.mouse_button, self.keys, self.delta_time, event_list)

            for surface in self.surfaces:
                self.screen.blit(surface, (0,0))

            for layout in self.layouts:
                layout.draw(self.screen, self.mouse_pos, self.mouse_button, self.keys, self.delta_time, event_list)

            # fps management
            self.fps.fps()
            self.fps.show_fps(self.screen)

            # flip screen at the end of scene
            pygame.display.flip()

            # delta time calcualtions
            current_frame_time = pygame.time.get_ticks()
            self.delta_time = (current_frame_time -
                               self.last_frame_time) / 1000.0
            self.last_frame_time = current_frame_time
            self.clock.tick(60)

        self.kill()

    def global_events(self, event_list) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    @staticmethod
    def kill() -> None:
        pygame.quit()

