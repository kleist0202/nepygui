import pygame
from .text import Static_Text, Dynamic_Text
from .colors import Colors
from abc import ABC, abstractmethod

class KeyArgumentNotFound(Exception):
    pass


class Widget(ABC):
    """ Base class of all GUI objects """

    def __init__(self, class_name="Widget", **kwargs):

        if class_name == __class__.__name__:
            self.check_options(kwargs)

        # positions and dimensions

        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.w = kwargs.get("w", 16)
        self.h = kwargs.get("h", 16)

    def recreate(self, **kwargs):
        self.x = kwargs.get("x", self.x)
        self.y = kwargs.get("y", self.y)
        self.w = kwargs.get("w", self.w)
        self.h = kwargs.get("h", self.h)

    def set_pos(self, x, y):
        self.recreate(x=x, y=y)

    def set_size(self, w, h):
        self.recreate(w=w, h=h)

    def get_pos(self):
        return (self.x, self.y)

    def get_size(self):
        return (self.w, self.h)

    @classmethod
    def check_options(cls, kwargs):
        for current_option in kwargs:
            if current_option not in cls.allowed_kwargs:
                raise KeyArgumentNotFound(current_option)

    @abstractmethod
    def draw(self, display=None, mouse_pos=0, mouse_button=0, keys=0, delta_time=0):
        pass


class Frame(Widget):
    """ Basic object which can be drawn on screen"""

    allowed_kwargs = [
        "x", "y", "w", "h",
        "fill", "bordercolor", "hover",
        "hovercolor", "gradient", "borderthickness",
        "gradientstart", "gradientend"
    ]


    def __init__(self, class_name="Frame", **kwargs):
        """
        Kwargs:
            **x (int): x position
            **y (int): y position
            **w (int): width
            **h (int): height
            **fill (tuple): background color of frame
            **bordercolor (tuple): color of border, border argument must be True
            **hover (bool): draw when hovering over or not
            **hovercolor (tuple): color which appear when mouse is hovering over frame
            **gradient (bool): draw gradient or not
            **gradientstart (tuple): set gradient start color 
            **gradientend (tuple):  set gradient end color
            **borderthickness (int): size of border
        """

        if class_name == __class__.__name__:
            self.check_options(kwargs)

        super().__init__("Frame", **kwargs)

        # new settings
        self.fill_color = kwargs.get("fill", Colors.White)
        self.border_color = kwargs.get("bordercolor", Colors.Gray)
        self.is_hover = kwargs.get("hover", False)
        self.hover_color = kwargs.get("hovercolor", self.fill_color)
        self.is_gradient = kwargs.get("gradient", False)
        self.gradient_start_color = kwargs.get("gradientstart", self.fill_color)
        self.gradient_end_color = kwargs.get("gradientend", tuple(map(lambda x: x - 60, self.fill_color)))
        self.border_thickness = kwargs.get("borderthickness", 0)
        self.hidden = False
        self.surf_init()

    def recreate(self, **kwargs):
        super().recreate(**kwargs)
        self.fill_color = kwargs.get("fill", self.fill_color)
        self.border_color = kwargs.get("bordercolor", self.border_color)
        self.is_hover = kwargs.get("hover", self.is_hover)
        self.hover_color = kwargs.get("hovercolor", self.hover_color)
        self.is_gradient = kwargs.get("gradient", self.is_gradient)
        self.gradient_start_color = kwargs.get("gradientstart", self.gradient_start_color)
        self.gradient_end_color = kwargs.get("gradientend", self.gradient_end_color)
        self.border_thickness = kwargs.get("borderthickness", self.border_thickness)
        self.surf_init()

    def surf_init(self):
        self.fill_surface = ColorSurface(self.fill_color, self.w, self.h)
        self.hover_surface = ColorSurface(self.hover_color, self.w, self.h)
        self.temp_fill_surface = self.fill_surface
        self.grad_surface = Gradient(self.gradient_start_color, self.gradient_end_color, self.w, self.h)
        self.temp_grad_surface = self.grad_surface

    def draw(self, display, mouse_pos, mouse_button=0, keys=0, delta_time=0, event_list=[]):
        if self.hidden:
            return
        if self.is_gradient:
            Special_Functions.border_rect(display, self.grad_surface.get_surface(),
                                          self.border_color, self.x, self.y, self.w, self.h, self.border_thickness)
        else:
            Special_Functions.border_rect(display, self.fill_surface.get_surface(),
                                          self.border_color, self.x, self.y, self.w, self.h, self.border_thickness)
        self.is_hovering(mouse_pos)

    def is_hovering(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[1] > self.y and mouse_pos[0] < self.x + self.w and mouse_pos[1] < self.y + self.h:
            if self.is_hover:
                self.fill_surface = self.hover_surface
                self.grad_surface = self.hover_surface
            else:
                self.fill_surface = self.temp_fill_surface
                self.grad_surface = self.temp_grad_surface
        else:
            self.fill_surface = self.temp_fill_surface
            self.grad_surface = self.temp_grad_surface

    def hide(self, flag):
        self.hidden = flag


class Label(Widget):
    """Creates label where you can display some text"""

    allowed_kwargs = ["x", "y", "w", "h",
                        "text", "anchor", "fontcolor", "fontsize", "bold"]

    def __init__(self, class_name="Label", **kwargs):
        """
        Kwargs:
            **x (int): x position
            **y (int): y position
            **w (int): width
            **h (int): height
            **text (str): text to display
            **anchor (str): set relative text position
            **fontcolor (tuple): changes font color
            **fontsize (int): set size of font
            **bold (bool): set text bold or not
        """

        if class_name == __class__.__name__:
            self.check_options(kwargs)

        super().__init__("Label", **kwargs)

        # new settings
        self.text = kwargs.get("text", "")
        self.anchor = kwargs.get("anchor", "C")
        self.font_color = kwargs.get("fontcolor", (0, 0, 0))
        self.font_size = kwargs.get("fontsize", 12)
        self.set_bold = kwargs.get("bold", False)

        self.text_object = Static_Text(
            fontsize=self.font_size, bold=self.set_bold, text=self.text, fontcolor=self.font_color)

        self.text_padding = 4
        # FIXME: There is no vertical padding

    def draw(self, display, mouse_pos=0, mouse_key=0, keys=0, delta_time=0, event_list=[]):
        vertical_center = self.y + self.h / 2 - self.text_object.get_text_height() / 2
        horizontal_center = self.x + self.w / 2 - self.text_object.get_text_width() / 2

        if self.anchor == "C":
            # center
            x_pos = horizontal_center
            y_pos = vertical_center
        elif self.anchor == "W":
            # left
            x_pos = self.x + self.text_padding
            y_pos = vertical_center
        elif self.anchor == "E":
            # right
            x_pos = self.x + self.w - self.text_object.get_text_width() - self.text_padding
            y_pos = vertical_center
        elif self.anchor == "N":
            # up
            x_pos = horizontal_center
            y_pos = self.y
        elif self.anchor == "S":
            # bottom
            x_pos = horizontal_center
            y_pos = self.y + self.h - self.text.get_text_height()
        elif self.anchor in ["NW", "WN"]:
            # up left
            x_pos = self.x + self.text_padding
            y_pos = self.y
        elif self.anchor in ["SW", "WS"]:
            # down left
            x_pos = self.x + self.text_padding
            y_pos = self.y + self.h - self.text_object.get_text_height()
        elif self.anchor in ["NE", "EN"]:
            # up right
            x_pos = self.x + self.w - self.text_object.get_text_width() - self.text_padding
            y_pos = self.y
        elif self.anchor in ["SE", "ES"]:
            # down right
            x_pos = self.x + self.w - self.text_object.get_text_width() - self.text_padding
            y_pos = self.y + self.h - self.text_object.get_text_height()
        else:
            x_pos = horizontal_center
            y_pos = vertical_center

        display.blit(self.text_object.get_surface(), (x_pos, y_pos))

    def set_padding(self, padd):
        self.text_padding = padd

    def get_padding(self):
        return self.text_padding

    def set_text(self, text):
        self.text = text
        self.text_object = Static_Text(
            h=self.h, text=text, fontsize=self.font_size, bold=self.set_bold, fontcolor=self.font_color)

    def set_color(self, color):
        self.font_color = color
        self.text_object = Static_Text(
            h=self.h, text=self.text, fontsize=self.font_size, bold=self.set_bold, fontcolor=color)

    def get_text(self):
        return self.text


class TextFrame(Frame, Label):
    """Creates frame with text to display"""

    allowed_kwargs = [
        "x", "y", "w", "h", "fill", "bordercolor",
        "hover", "hovercolor", "gradient", "text", "align",
        "borderthickness", "anchor", "fontcolor", "fontsize", "bold",
        "gradientstart", "gradientend"]


    def __init__(self, class_name="TextFrame", **kwargs):
        """
        Kwargs:
            **x (int): x position
            **y (int): y position
            **w (int): width
            **h (int): height
            **fill (tuple): background color of frame
            **bordercolor (tuple): color of border, border argument must be True
            **hover (bool): draw when hovering over or not
            **hovercolor (tuple): color which appear when mouse is hovering over frame
            **gradient (bool): draw gradient or not
            **text (str): text to display
            **align (str): align text ("left", "center", "right")
            **border_thickness (int): size of border
            **anchor (str): set relative text position
            **fontcolor (tuple): changes font color
            **fontsize (int): set size of font
            **bold (bool): set text bold or not
        """

        if class_name == __class__.__name__:
            self.check_options(kwargs)

        super().__init__("TextFrame", **kwargs)

        if self.w < self.text_object.get_text_width():
            self.w = self.text_object.get_text_width()
            Frame.recreate(self, w=self.w, h=self.h)

        if self.h < self.text_object.get_text_height():
            self.h = self.text_object.get_text_height()
            Frame.recreate(self, w=self.w, h=self.h)

        Label.set_padding(self, Label.get_padding(self)
                          + self.border_thickness/2)

    def draw(self, display, mouse_pos, mouse_key=0, keys=0, delta_time=0, event_list=[]):
        if self.hidden:
            return
        Frame.draw(self, display, mouse_pos)
        Label.draw(self, display)


class AbstractButton(Widget):
    """ Class which provides functionality common to buttons """

    def __init__(self, class_name="AbstractButton", **kwargs):
        super().__init__("AbstractButton", **kwargs)
        self.pressed = False
        self.function = kwargs.get("func", None)

    def is_clicked(self, mouse_pos, mouse_key):

        # we are checking if mouse position covers button dimensions
        if mouse_pos[0] > self.x and mouse_pos[1] > self.y and mouse_pos[0] < self.x + self.w and mouse_pos[1] < self.y + self.h:
            if not mouse_key[0]:
                if self.pressed:
                    if self.function == None:
                        pass
                    else:
                        self.function(self)

            # when mouse hover on the button, we can check if mouse button is pressed and trigger an event
            if mouse_key[0]:
                if not self.pressed:
                    self.pressed = True
                return True

        self.pressed = False
        return False


class Button(AbstractButton, TextFrame):
    """Class which allows you to draw fully functional button"""

    allowed_kwargs = [
        "x", "y", "w", "h", "fill", "bordercolor",
        "hover", "hovercolor", "pressedcolor", "gradient",
        "text", "align", "borderthickness", "anchor", "fontcolor",
        "gradientstart", "gradientend",
        "fontsize", "bold", "func"]


    def __init__(self, class_name="Button", **kwargs):
        """
        Kwargs:
            **x (int): x position
            **y (int): y position
            **w (int): width
            **h (int): height
            **fill (tuple): background color of button
            **bordercolor (tuple): color of border, border argument must be True
            **hover (bool): change color when hovering over or not
            **hovercolor (tuple): color which appear when mouse is hovering over button
            **pressedcolor (tuple): color which appear when button is pressed
            **gradient (bool): draw gradient or not
            **text (str): text to display
            **align (str): align text ("left", "center", "right")
            **borderthickness (int): size of border
            **anchor (str): set relative text position
            **fontcolor (tuple): changes font color
            **fontsize (int): set size of font
            **bold (bool): set text bold or not
            **func (function): function which will be executed when the button is pressed
        """

        if class_name == __class__.__name__:
            self.check_options(kwargs)

        super().__init__("Button", **kwargs)

        # new settings
        self.color_pressed = kwargs.get("pressedcolor", Colors.LightGray)
        self.color_surface_pressed = ColorSurface(
            self.color_pressed, self.w, self.h)

        # default settings
        self.is_gradient = kwargs.get("gradient", True)
        self.border_thickness = kwargs.get("borderthickness", 2)
        self.clicking_blocked = False

    def recreate(self, **kwargs):
        super().recreate(**kwargs)
        self.color_surface_pressed = ColorSurface(self.color_pressed, self.w, self.h)

    def draw(self, display, mouse_pos, mouse_key, keys=0, delta_time=0, event_list=[]):
        if self.hidden:
            return
        TextFrame.draw(self, display, mouse_pos)
        if self.clicking_blocked:
            return
        if(super().is_clicked(mouse_pos, mouse_key)):
            self.fill_surface = self.color_surface_pressed
            self.grad_surface = self.color_surface_pressed

    def block(self, flag):
        self.clicking_blocked = flag

    def __repr__(self):
        return __class__.__name__


class AbstractEntry(Widget):
    """Class which provides functionality of writing text"""

    press_delay = 0.2
    blit_delay = 0.5
    banned_keys = [pygame.K_BACKSPACE, pygame.K_ESCAPE]

    def __init__(self, class_name="AbstractEntry", **kwargs):
        super().__init__(**kwargs)
        self.entry_value = ""
        self.dyn_text = Dynamic_Text(x=self.x, y=self.y, h=self.h)
        self.name = []
        self.marker_x = 0

        # set marker step for entry
        self.marker_step = self.dyn_text.get_letter_size()/2

        self.current_step = 0
        self.current_key = None
        self.current_blit_time = AbstractEntry.blit_delay
        self.current_press_time = 0

    def writing(self, display, keys, delta_time, event_list):
        self.marker_x = self.x + self.w / 2 + self.current_step
        self.blitting_line(display, delta_time)

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.name:
                    self.current_key = event
                    self.name.pop()
                    self.current_step -= self.marker_step
                    self.current_press_time = 0
                    self.current_blit_time = AbstractEntry.blit_delay
                else:
                    if event.key not in AbstractEntry.banned_keys:
                        if self.marker_x + self.marker_step >= self.x + self.w:
                            return

                        self.current_key = event
                        self.name.append(event.unicode)
                        self.current_step += self.marker_step
                        self.current_press_time = 0
                        self.current_blit_time = AbstractEntry.blit_delay

        if self.current_press_time >= AbstractEntry.press_delay:
            self.current_press_time = 0
            if self.current_key is not None:
                if self.current_key.key not in AbstractEntry.banned_keys:
                    if keys[self.current_key.key]:
                        if self.marker_x + self.marker_step >= self.x + self.w:
                            return
                        self.name.append(self.current_key.unicode)
                        self.current_step += self.marker_step
                        self.current_blit_time = AbstractEntry.blit_delay
                else:
                    if keys[self.current_key.key] and self.name:
                        if self.marker_x + self.marker_step >= self.x + self.w:
                            return
                        self.name.pop()
                        self.current_step -= self.marker_step
                        self.current_blit_time = AbstractEntry.blit_delay


        self.current_press_time += 1 * delta_time

    def blitting_line(self, display, delta_time):
        if self.current_blit_time > AbstractEntry.blit_delay:
            pygame.draw.line(display, Colors.Black, (self.marker_x,
                             self.y + 8), (self.marker_x, self.y + self.h - 8))
            if self.current_blit_time > AbstractEntry.blit_delay * 2:
                self.current_blit_time = 0
        self.current_blit_time += 1 * delta_time

    def clear_entry_value(self):
        self.entry_value = ""
        self.name.clear()
        self.marker_x = self.x + self.w / 2

    def set_entry_value(self, value):
        self.entry_value = ""
        self.name.clear()
        self.name = list(value)
        self.entry_value = value
        self.current_step = self.marker_step * len(self.name)

    def get_entry_value(self):
        return self.entry_value


class EntryWidget(AbstractEntry, AbstractButton, Frame):
    """Creates entry which allows you to write some text"""

    allowed_kwargs = [
        "x", "y", "w", "h", "fill", "bordercolor",
        "hover", "hovercolor", "gradient", "borderthickness",
        "activebordercolor"]

    def __init__(self, class_name="EntryWidget", **kwargs):
        """
        Kwargs:
            **x (int): x position
            **y (int): y position
            **w (int): width
            **h (int): height
            **fill (tuple): background color of entry
            **bordercolor (tuple): color of border, border argument must be True
            **hover (bool): change color when hovering over or not
            **hovercolor (tuple): color which appear when mouse is hovering over entry
            **gradient (bool): draw gradient or not
            **borderthickness (int): size of border
            **activebordercolor (tuple): border color which appear when entry is active 
        """

        if class_name == __class__.__name__:
            self.check_options(kwargs)

        super().__init__("EntryWidget", **kwargs)

        self.is_active = False
        self.prev_active_border_color = self.border_color

        # default settings
        self.active_border_color = kwargs.get(
            "activebordercolor", Colors.SkyBlue)
        self.border_thickness = kwargs.get("borderthickness", 2)

        # entrywidget as 'abstractbutton', needs function: here, activate entry
        self.function = self.activate

    def draw(self, display, mouse_pos, mouse_key, keys, delta_time, event_list):
        if self.hidden:
            return
        AbstractButton.is_clicked(self, mouse_pos, mouse_key)
        Frame.draw(self, display, mouse_pos)
        if self.is_active:
            self.border_color = self.active_border_color
            AbstractEntry.writing(self, display, keys, delta_time, event_list)
        else:
            self.border_color = self.prev_active_border_color
        self.entry_value = "".join(self.name)
        self.dyn_text.render_text(display, self.entry_value, self.w, self.h)

        # when we press mouse button outside entry, it deactivates itself
        if mouse_pos[0] < self.x or mouse_pos[0] > self.x + self.w or mouse_pos[1] < self.y or mouse_pos[1] > self.y + self.h:
            if mouse_key[0]:
                self.deactivate()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.current_blit_time = AbstractEntry.blit_delay 
        self.is_active = False

    def recreate(self, **kwargs):
        Frame.recreate(self, **kwargs)
        self.dyn_text.recreate(**kwargs)


# --------------------------------------------------------------------- #


class Special_Functions:
    """Helpful functions which can help make code cleaner"""

    def __init__(self): pass

    @staticmethod
    def border_rect(display, color_surface, frame_color, x, y, w, h, border_thickness):
        """Function which allows you draw rectangle with borders"""
        display.blit(color_surface, (x, y))
        pygame.draw.line(display, frame_color, (x, y),
                         (x + w, y), border_thickness)
        pygame.draw.line(display, frame_color,
                         (x, y + h), (x + w, y + h), border_thickness)
        pygame.draw.line(display, frame_color, (x, y),
                         (x, y + h), border_thickness)
        pygame.draw.line(display, frame_color,
                         (x + w, y), (x + w, y + h), border_thickness)


class ColorSurface:
    """Class which gives you rectangular surfaces of the selected color"""

    def __init__(self, color, w, h):
        self.clr_surface = pygame.Surface(
            (w, h), pygame.HWSURFACE)
        self.color_surface(color, w, h)

    def color_surface(self, color, w, h):
        pygame.draw.rect(self.clr_surface, color, (0, 0, w, h))

    def get_surface(self):
        return self.clr_surface


class Gradient:
    """Class which calculates surface with gradient"""

    def __init__(self, begin, end, w, h, orientation="vertical"):
        self.gradient_surface = pygame.Surface((w, h), pygame.HWSURFACE)
        if orientation == "vertical":
            self.vertical_gradient(self.gradient_surface, begin, end, w, h)
        else:
            self.horizontal_gradient(self.gradient_surface, begin, end, w, h)

    def vertical_gradient(self, surface, begin, end, w, h):
        begin_red, begin_green, begin_blue = begin
        end_red, end_green, end_blue = end 
        for layer in range(h):
            r = begin_red + layer/h * (end_red - begin_red);
            g = begin_green + layer/h * (end_green - begin_green);
            b = begin_blue + layer/h * (end_blue - begin_blue);
            pygame.draw.line(surface,
                             (self.to_zero(r),
                              self.to_zero(g),
                              self.to_zero(b)),
                             (0, 0 + layer), (0 + w, 0 + layer), 1)

    def horizontal_gradient(self, surface, begin, end, w, h):
        begin_red, begin_green, begin_blue = begin
        end_red, end_green, end_blue = end 
        for layer in range(h):
            r = begin_red + layer/h * (end_red - begin_red);
            g = begin_green + layer/h * (end_green - begin_green);
            b = begin_blue + layer/h * (end_blue - begin_blue);
            pygame.draw.line(surface,
                             (self.to_zero(r),
                              self.to_zero(g),
                              self.to_zero(b)),
                             (0 + layer, 0), (0 + layer, 0 + h), 1)

    def get_surface(self):
        return self.gradient_surface

    def to_zero(self, v):
        if v < 0:
            return 0
        else:
            return v
