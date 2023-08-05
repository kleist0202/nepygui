import pygame
from .fps import Fps
from. layouts import Layout

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

        self.clock = pygame.time.Clock()
        self.fps = Fps()

        self.delta_time = 0
        self.mouse_button = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()

        self.last_frame_time = pygame.time.get_ticks()

        self.current_menu = "default"
        self.menus_dict = {self.current_menu: []}
        self.current_menu_list = []
        self.switch_menus("default")
        self.resize_callback_func = lambda: None

    def window_resize_callback(self, screen_size, func):
        if self.window_size[0] != screen_size[0]:
            func()
        elif self.window_size[1] != screen_size[1]:
            func()

    def add_to_menu(self, widget, menu_name="default"):
        if menu_name not in self.menus_dict:
            self.menus_dict[menu_name] = []
        self.menus_dict[menu_name].append(widget)

    def switch_menus(self, menu_name):
        self.current_menu = menu_name
        self.current_menu_list = self.menus_dict.get(self.current_menu, self.menus_dict["default"])

        for layout in self.current_menu_list:
            if isinstance(layout, Layout):
                layout.put()

    def init_window(self):
        pygame.display.set_caption(self.caption)

        if self.fullscreen:
            self.window_size = (0, 0)
            self.options |= pygame.FULLSCREEN

        if self.resizable:
            self.options |= pygame.RESIZABLE

        self.screen = pygame.display.set_mode(self.window_size, self.options)
        
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
        if self.screen is None:
            print("You forgot to initialize window! Call init_window() function before calling main_loop().")
            return

        while self.running:
            event_list = pygame.event.get()
            self.window_resize_callback(self.screen.get_size(), self.resize_callback_func)
            self.window_size = self.screen.get_size()
            self.global_events(event_list)
            self.screen.fill(self.screen_color)

            # ------------ scene ------------- #

            # get mouse and keyboard input
            self.mouse_button = pygame.mouse.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            self.keys = pygame.key.get_pressed()

            for widget in self.current_menu_list:
                widget.draw(self.screen, self.mouse_pos, self.mouse_button, self.keys, self.delta_time, event_list)

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

    def global_events(self, event_list) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def exit(self) -> None:
        self.running = False
