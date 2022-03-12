# --------------------------------------------------------------------- #
# -----------------------------LAYOUTS--------------------------------- #
# --------------------------------------------------------------------- #

from abc import ABC, abstractmethod


class Layout(ABC):
    """A"""
    @abstractmethod
    def __init__(self, window):
        self.widgets = []
        self.w = window
        self.x_size, self.y_size = window.get_size()

    @abstractmethod
    def add_widget(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def resize(self):
        pass

    @abstractmethod
    def put(self):
        pass

    def window_resize_callback(func):
        def inner(self, screen, mouse_pos, mouse_button, keys, delta_time, event_list):
            x_size, y_size = self.w.get_size()
            if self.x_size != x_size:
                self.x_size = x_size
                self.resize()
            elif self.y_size != y_size:
                self.y_size = y_size
                self.resize()
            func(self, screen, mouse_pos, mouse_button, keys, delta_time, event_list)
        return inner


class VLayout(Layout):
    def __init__(self, window, orientation="NW", x_start=0, y_start=0):
        super().__init__(window)
        self.orientation = orientation
        self.x_start = x_start
        self.y_start = y_start
        self.keep_padd_info = []
        self.curr_x = 0
        self.curr_y = 0
        self.greatest_width = 0

    def add_widget(self, widget, ypadd=0):
        self.widgets.append(widget)
        self.keep_padd_info.append(ypadd)
        self.greatest_width = (max(widget.w for widget in self.widgets))

        # adjust every widget to greatest width
        for curr_widget in self.widgets:
            _, curr_h = curr_widget.get_size()
            curr_widget.set_size(self.greatest_width, curr_h)

    @Layout.window_resize_callback
    def draw(self, screen, mouse_pos, mouse_button, keys, delta_time, event_list):

        for widget in self.widgets:
            widget.draw(screen, mouse_pos, mouse_button, keys, delta_time, event_list)

    def put(self):
        # jesus... this code is too complicated and probably bloated
        # at least it works
        for i, widget in enumerate(self.widgets):
            curr_w, curr_h = widget.get_size()

            # bloated
            if self.orientation == "C":
                if i == 0:
                    self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                    for j, curr_widget in enumerate(self.widgets):
                        _, curr_h2 = curr_widget.get_size()
                        if j != 0:
                            self.curr_y -= curr_h2/2 + self.keep_padd_info[j]/2
                        else:
                            self.curr_y -= self.keep_padd_info[j]/2

                self.curr_x = self.x_size/2 - curr_w/2 + self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # no need to bloat
            elif self.orientation == "N":
                if i == 0:
                    self.curr_y = self.y_start
                self.curr_x = self.x_size/2 - curr_w/2 + self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation == "S":
                if i == 0:
                    self.curr_y = self.y_size - curr_h + self.y_start
                    for j, curr_widget in enumerate(self.widgets):
                        _, curr_h2 = curr_widget.get_size()
                        if j != 0:
                            self.curr_y -= curr_h2 + self.keep_padd_info[j]
                        else:
                            self.curr_y -= self.keep_padd_info[j]
                self.curr_x = self.x_size/2 - curr_w/2 + self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation == "W":
                if i == 0:
                    self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                    for j, curr_widget in enumerate(self.widgets):
                        _, curr_h2 = curr_widget.get_size()
                        if j != 0:
                            self.curr_y -= curr_h2/2 + self.keep_padd_info[j]/2
                        else:
                            self.curr_y -= self.keep_padd_info[j]/2
                self.curr_x = self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation == "E":
                if i == 0:
                    self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                    for j, curr_widget in enumerate(self.widgets):
                        _, curr_h2 = curr_widget.get_size()
                        if j != 0:
                            self.curr_y -= curr_h2/2 + self.keep_padd_info[j]/2
                        else:
                            self.curr_y -= self.keep_padd_info[j]/2
                self.curr_x = self.x_size - curr_w + self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # no need to bloat
            elif self.orientation in ["EN", "NE"]:
                if i == 0:
                    self.curr_y = self.y_start
                self.curr_x = self.x_size - curr_w + self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # no need to bloat
            elif self.orientation in ["NW", "WN"]:
                if i == 0:
                    self.curr_y = self.y_start
                self.curr_x = self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation in ["SW", "WS"]:
                if i == 0:
                    self.curr_y = self.y_size - curr_h + self.y_start
                    for j, curr_widget in enumerate(self.widgets):
                        _, curr_h2 = curr_widget.get_size()
                        if j != 0:
                            self.curr_y -= curr_h2 + self.keep_padd_info[j]
                        else:
                            self.curr_y -= self.keep_padd_info[j]
                self.curr_x = self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation in ["SE", "ES"]:
                if i == 0:
                    self.curr_y = self.y_size - curr_h + self.y_start
                    for j, curr_widget in enumerate(self.widgets):
                        _, curr_h2 = curr_widget.get_size()
                        if j != 0:
                            self.curr_y -= curr_h2 + self.keep_padd_info[j]
                        else:
                            self.curr_y -= self.keep_padd_info[j]

                self.curr_x = self.x_size - curr_w + self.x_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            self.curr_y += curr_h + self.keep_padd_info[i]

    def resize(self):
        self.put()


class HLayout(Layout):
    def __init__(self, window, orientation="NW", x_start=0, y_start=0):
        super().__init__(window)
        self.orientation = orientation
        self.x_start = x_start
        self.y_start = y_start
        self.keep_padd_info = []
        self.curr_x = 0
        self.curr_y = 0
        self.greatest_height = 0

    def add_widget(self, widget, ypadd=0):
        self.widgets.append(widget)
        self.keep_padd_info.append(ypadd)
        self.greatest_height = max(widget.h for widget in self.widgets)

        # adjust every widget to greatest height
        for curr_widget in self.widgets:
            curr_w, _ = curr_widget.get_size()
            curr_widget.set_size(curr_w, self.greatest_height)

    @Layout.window_resize_callback
    def draw(self, screen, mouse_pos, mouse_button, keys, delta_time, event_list):

        for widget in self.widgets:
            widget.draw(screen, mouse_pos, mouse_button, keys, delta_time, event_list)

    def put(self):
        for i, widget in enumerate(self.widgets):
            curr_w, curr_h = widget.get_size()

            # bloated
            if self.orientation == "C":
                if i == 0:
                    self.curr_x = self.x_size/2 - curr_w/2 + self.x_start
                    for j, curr_widget in enumerate(self.widgets):
                        curr_w2, _ = curr_widget.get_size()
                        if j != 0:
                            self.curr_x -= curr_w2/2 + self.keep_padd_info[j]/2
                        else:
                            self.curr_x -= self.keep_padd_info[j]/2
                self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # no need to bloat
            elif self.orientation == "W":
                if i == 0:
                    self.curr_x = self.x_start
                self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation == "E":
                if i == 0:
                    self.curr_x = self.x_size - curr_w + self.x_start
                    for j, curr_widget in enumerate(self.widgets):
                        curr_w2, _ = curr_widget.get_size()
                        if j != 0:
                            self.curr_x -= curr_w2 + self.keep_padd_info[j]
                        else:
                            self.curr_x -= self.keep_padd_info[j]
                self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation == "N":
                if i == 0:
                    self.curr_x = self.x_size/2 - curr_w/2 + self.x_start
                    for j, curr_widget in enumerate(self.widgets):
                        curr_w2, _ = curr_widget.get_size()
                        if j != 0:
                            self.curr_x -= curr_w2/2 + self.keep_padd_info[j]/2
                        else:
                            self.curr_x -= self.keep_padd_info[j]/2
                self.curr_y = self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation == "S":
                if i == 0:
                    self.curr_x = self.x_size/2 - curr_w/2 + self.x_start
                    for j, curr_widget in enumerate(self.widgets):
                        curr_w2, _ = curr_widget.get_size()
                        if j != 0:
                            self.curr_x -= curr_w2/2 + self.keep_padd_info[j]/2
                        else:
                            self.curr_x -= self.keep_padd_info[j]/2
                self.curr_y = self.y_size - curr_h + self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # no need to bloat
            elif self.orientation in ["SW", "WS"]:
                if i == 0:
                    self.curr_x = self.x_start
                self.curr_y = self.y_size - curr_h + self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # no nedd to bloat
            elif self.orientation in ["NW", "WN"]:
                if i == 0:
                    self.curr_x = self.x_start
                self.curr_y = self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            # bloated
            elif self.orientation in ["EN", "NE"]:
                if i == 0:
                    self.curr_x = self.x_size - curr_w + self.x_start
                    for j, curr_widget in enumerate(self.widgets):
                        curr_w2, _ = curr_widget.get_size()
                        if j != 0:
                            self.curr_x -= curr_w2 + self.keep_padd_info[j]
                        else:
                            self.curr_x -= self.keep_padd_info[j]
                self.curr_y = self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            elif self.orientation in ["SE", "ES"]:
                if i == 0:
                    self.curr_x = self.x_size - curr_w + self.x_start
                    for j, curr_widget in enumerate(self.widgets):
                        curr_w2, _ = curr_widget.get_size()
                        if j != 0:
                            self.curr_x -= curr_w2 + self.keep_padd_info[j]
                        else:
                            self.curr_x -= self.keep_padd_info[j]
                self.curr_y = self.y_size - curr_h + self.y_start
                widget.set_pos(self.curr_x,
                               self.curr_y)

            self.curr_x += curr_w + self.keep_padd_info[i]

    def resize(self):
        self.put()

# --------------------------------------------------------------------- #

class GridLayout(Layout):
    def __init__(self, window, orientation="NW", x_start=0, y_start=0):
        super().__init__(window)
        self.orientation = orientation
        self.x_start = x_start
        self.y_start = y_start
        self.curr_x = 0
        self.curr_y = 0
        self.main_x = 0
        self.keep_padd_info = []
        self.pre_widgets = []

    def add_widget(self, widget, row, col, xpadd=0, ypadd=0):
        self.widgets = [[None]]
        self.pre_widgets.append([widget, row, col])
        self.greatest_width = max(widget[0].w for widget in self.pre_widgets)
        self.greatest_height = max(widget[0].h for widget in self.pre_widgets)

        for pre_widget in self.pre_widgets:
            self.set_order(*pre_widget)

        for r in self.widgets[:]:
            if all(e is None for e in r):
                self.widgets.remove(r)

        r = 0
        while True:
            longest_length = max([len(a) for a in self.widgets])
            c = self.get_column(self.widgets, r)
            if all(e is None for e in c):
                for j in self.widgets:
                    del j[r]
                r = 0
            else:
                r += 1
            if r >= longest_length:
                break
            
        # adjust every widget to greatest width and height
        for curr_widget_r in self.widgets:
            for curr_widget in curr_widget_r:
                if curr_widget is None:
                    continue
                curr_widget.set_size(self.greatest_width, self.greatest_height)


    def set_order(self, widget, row=0, col=0):
        if row > col:
            asd = row
        else:
            asd = col

        while asd >= len(self.widgets):
            self.widgets.append([None])
        
        for r in self.widgets:
            while asd >= len(r):
                r.append(None)
        
        self.widgets[row][col] = widget

    @Layout.window_resize_callback
    def draw(self, screen, mouse_pos, mouse_button, keys, delta_time, event_list):
        for widget_r in self.widgets:
            for widget in widget_r:
                if widget is None:
                    continue
                widget.draw(screen, mouse_pos, mouse_button, keys, delta_time, event_list)


    def put(self):
        for i, widgets_r in enumerate(self.widgets):
            for j, widget in enumerate(widgets_r):
                if widget is None:
                    self.curr_x += self.greatest_width
                    continue
                curr_w, curr_h = widget.get_size()

                # bloated
                if self.orientation == "C":
                    if i == 0 and j == 0:
                        self.curr_x = self.x_size/2 - curr_w/2 + self.x_start
                        self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                        for k, widgets_r2 in enumerate(self.widgets):
                            for l, curr_widget in enumerate(widgets_r2):
                                if curr_widget is None:
                                    continue
                            if k != 0:
                                self.curr_x -= self.greatest_width/2
                                self.curr_y -= self.greatest_height/2
                        self.main_x = self.curr_x
                    widget.set_pos(self.curr_x,
                                   self.curr_y)

                elif self.orientation == "W":
                    if i == 0 and j == 0:
                        self.curr_x = self.x_start
                        self.curr_y = self.y_size/2 - curr_h/2 + self.y_start
                        for k, curr_widget_r in enumerate(self.widgets):
                            rows = len(curr_widget_r)
                            for l, curr_widget in enumerate(curr_widget_r):
                                if curr_widget is None:
                                     continue
                            if k != 0:
                                self.curr_y -= self.greatest_height/2
                        self.main_x = self.curr_x
                    widget.set_pos(self.curr_x,
                                   self.curr_y)

                self.curr_x += curr_w

            self.curr_x = self.main_x
            self.curr_y += curr_h

    def resize(self):
        self.put()

    @staticmethod
    def get_column(l, col):
        a = [[x for i, x in enumerate(a) if i == col] for a in l]
        a = [j for sub in a for j in sub]
        return a

    @staticmethod
    def cool_print(m):
        print('[')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in m]))
        print(']')

# --------------------------------------------------------------------- #
