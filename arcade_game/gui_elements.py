import arcade
import typing


class Button:
    def __init__(self, center_x, center_y, width, height, action_function):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.action_function = action_function
        self.pressed = False
        self.enabled = True

    def on_press(self):
        if self.enabled:
            self.pressed = True

    def on_release(self):
        self.pressed = False
        self.action_function()

    def check_mouse_press(self, x, y):
        if x > self.center_x + self.width / 2:
            return False
        if x < self.center_x - self.width / 2:
            return False
        if y > self.center_y + self.height / 2:
            return False
        if y < self.center_y - self.height / 2:
            return False
        return True

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True


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


class ButtonSprite(arcade.Sprite, Button):
    def __init__(self, filename, scale, center_x, center_y, action_function):
        arcade.Sprite.__init__(self, filename=filename, center_x=center_x, center_y=center_y, scale=scale)

        Button.__init__(self, center_x=center_x, center_y=center_y, width=self.width, height=self.height,
                        action_function=action_function)


class ActionSprite(ButtonSprite):
    def __init__(self, filename, scale, center_x, center_y, action_function):
        super().__init__(filename, scale, center_x, center_y, action_function)

    # Should handle selection and when the button is enabled for clicking.

    def change_texture(self):
        pass

    def reset_selection(self):
        pass


# This is for type hinting to also accept SpriteButton instances and not just Sprites.
T = typing.TypeVar('T', bound=ButtonSprite)


class ButtonSpriteList(arcade.SpriteList):
    def __init__(self):
        super().__init__()

    def __iter__(self) -> typing.Iterable[T]:
        return iter(self.sprite_list)

    def check_press(self, x, y):
        for sp in self.sprite_list:
            if sp.check_mouse_press(x, y):
                sp.on_press()

    def check_release(self):
        for sp in self.sprite_list:
            if sp.pressed:
                sp.on_release()



