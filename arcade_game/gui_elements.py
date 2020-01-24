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
        self.visible = True

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

    def set_enabled(self, param: bool):
        self.enabled = param

    def set_visible(self, param: bool):
        self.visible = param


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


class ButtonSprite(arcade.Sprite, Button):
    def __init__(self, filename, scale, center_x, center_y, action_function):
        arcade.Sprite.__init__(self, filename=filename, center_x=center_x, center_y=center_y, scale=scale)

        Button.__init__(self, center_x=center_x, center_y=center_y, width=self.width, height=self.height,
                        action_function=action_function)

    def draw(self):
        if self.visible:
            arcade.Sprite.draw(self)


class ActionSprite(ButtonSprite):
    def __init__(self, filename, scale, center_x, center_y, action_function,
                 start_visible: bool = True, start_enabled: bool = True, disabled_texture=None):
        super().__init__(filename, scale, center_x, center_y, action_function)

        self.set_visible(start_visible)
        self.set_enabled(start_enabled)

        if disabled_texture is not None:
            self.append_texture(arcade.load_texture(disabled_texture, scale=self.scale))

    def set_enabled(self, param: bool):
        super().set_enabled(param)
        try:
            self.set_texture(int(param))
        except:
            pass

    def reset_selection(self):
        pass


# This is for type hinting to also accept SpriteButton instances and not just Sprites.
T = typing.TypeVar('T', bound=ButtonSprite)


class ActionSpriteList:
    scale = 0.2

    def __init__(self, assets_path, game_window, opponent=False):

        if opponent:
            y = game_window.height - 60
        else:
            y = 60

        self.secret_btn = ActionSprite(filename=assets_path + 'secret.png', scale=self.scale,
                                       center_x=int(game_window.width / 1.5 + (0 - 3) * game_window.ACTION_SPACING),
                                       center_y=y,
                                       action_function=game_window.secret_pressed,
                                       start_enabled=False, start_visible=False,
                                       disabled_texture=assets_path + 'secret2.png')

        self.burn_btn = ActionSprite(filename=assets_path + 'burn.png', scale=self.scale,
                                     center_x=int(game_window.width / 1.5 + (1 - 3) * game_window.ACTION_SPACING),
                                     center_y=y,
                                     action_function=game_window.burn_pressed,
                                     start_enabled=False, start_visible=False,
                                     disabled_texture=assets_path + 'burn2.png')

        self.gift_btn = ActionSprite(filename=assets_path + 'gift.png', scale=self.scale,
                                     center_x=int(game_window.width / 1.5 + (2 - 3) * game_window.ACTION_SPACING),
                                     center_y=y,
                                     action_function=game_window.gift_pressed,
                                     start_enabled=False, start_visible=False,
                                     disabled_texture=assets_path + 'gift2.png')

        self.comp_btn = ActionSprite(filename=assets_path + 'comp.png', scale=self.scale,
                                     center_x=int(game_window.width / 1.5 + (3 - 3) * game_window.ACTION_SPACING),
                                     center_y=y,
                                     action_function=game_window.comp_pressed,
                                     start_enabled=False, start_visible=False,
                                     disabled_texture=assets_path + 'comp2.png')

        self.btn_lst = [self.secret_btn, self.burn_btn, self.gift_btn, self.comp_btn]
        self.available = (self.secret_btn, self.burn_btn, self.gift_btn, self.comp_btn)

    def check_press(self, x, y):
        for sp in self.btn_lst:
            if sp.check_mouse_press(x, y):
                sp.on_press()

    def check_release(self):
        pressed_count = 0
        for sp in self.btn_lst:
            if sp.pressed:
                pressed_count += 1
                sp.on_release()

        return pressed_count

    def draw(self):
        for sp in self.btn_lst:
            sp.draw()

    def all(self):
        return self.btn_lst

    def remove_availble(self, btn):
        self.available = tuple(x for x in self.available if x != btn)

    def not_secret(self):
        return [self.burn_btn, self.gift_btn,  self.comp_btn]

    def not_burn(self):
        return [self.secret_btn, self.gift_btn, self.comp_btn]

    def not_gift(self):
        return [self.secret_btn, self.burn_btn, self.comp_btn]

    def not_comp(self):
        return [self.secret_btn, self.burn_btn, self.gift_btn]
