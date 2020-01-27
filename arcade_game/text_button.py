import arcade


class Button:
    def __init__(self, center_x, center_y, width, height, action_function):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.action_function = action_function
        self.pressed = False
        self._enabled = True
        self._visible = True

        self.right = self.center_x + self.width / 2
        self.left = self.center_x - self.width / 2
        self.top = self.center_y + self.height / 2
        self.bottom = self.center_y - self.height / 2

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value

    def mouse_press(self, x, y):
        if self.is_click_inside(x, y) and self.enabled:
            self.pressed = True

    def mouse_release(self):
        if self.pressed:
            self.pressed = False
            self.action_function()

            return 1
        return 0

    def is_click_inside(self, x, y):
        if x > self.right:
            return False
        if x < self.left:
            return False
        if y > self.top:
            return False
        if y < self.bottom:
            return False
        return True


class TextBoxButton(Button):
    def __init__(self, text, center_x, center_y, width, height, action_function,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        super().__init__(center_x, center_y, width, height, action_function)

        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        if not self.visible:
            return

        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        text_x = self.center_x
        text_y = self.center_y

        if not self.pressed:
            text_x -= self.button_height
            text_y += self.button_height

        arcade.draw_text(self.text, text_x, text_y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")
