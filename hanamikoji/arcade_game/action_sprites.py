import arcade
import os


class ActionSprite(arcade.Sprite):
    HIGHLIGHT_COLOR = arcade.color.WHITE
    HIGHLIGHT_WIDTH = 2
    SCALE = 0.2

    def __init__(self, action: str, center_x: float, center_y: float, action_function):
        arcade.Sprite.__init__(self, filename=os.path.join('.', 'assets', 'actions', action + '.png'),
                               center_x=center_x, center_y=center_y, scale=self.SCALE)

        # These booleand controle the click-abality, texture display and selection:
        self._enable: bool = False
        self._used: bool = False
        self.pressed: bool = False
        self.selected: bool = False

        # Here: disabled and flipped textures: KEEP the ORDER
        self.append_texture(arcade.load_texture(
            file_name=os.path.join('.', 'assets', 'actions', action + '_disabled.png')))
        self.append_texture(arcade.load_texture(
            file_name=os.path.join('.', 'assets', 'actions', action + '_used.png')))

        self.action_function = action_function
        self.enabled = True

        # the string of the action
        self.value = action


    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        self.set_texture(int(not value))

    @property
    def used(self):
        return self._used

    @used.setter
    def used(self, value: bool):
        self._used = value

        self.enabled = False

        if self._used:
            self.set_texture(2)
        else:
            self.set_texture(int(not self.enabled))

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

    def mouse_press(self, x, y):
        if self.is_click_inside(x, y) and self.enabled:
            self.pressed = True

    def mouse_release(self):
        if self.pressed:
            self.pressed = False
            self.selected = not self.selected
            self.action_function()
            return True
        return False

    def draw(self):
        super().draw()

        if self.selected:
            arcade.draw_lrtb_rectangle_outline(self.left, self.right, self.top, self.bottom,
                                               color=self.HIGHLIGHT_COLOR, border_width=self.HIGHLIGHT_WIDTH)


class ActionSpriteManager:
    action_library = ('secret', 'burn', 'gift', 'comp')

    ACTION_HEIGHT = 60
    ACTION_SPACING = 120

    def __init__(self, parent_window: arcade.Window):
        self.parent_window = parent_window
        self.actions = {'player1': [], 'player2': []}
        self.action_indeces = {}
        self.callbacks = [parent_window.secret_pressed, parent_window.burn_pressed, parent_window.gift_pressed,
                          parent_window.comp_pressed]
        size = len(self.action_library)

        for idx, a in enumerate(self.action_library):
            self.actions['player1'].append(ActionSprite(action=a, action_function=self.callbacks[idx],
                                                        center_x=self.parent_window.width / 2 + (idx - (size - 1) / 2)
                                                                 * self.ACTION_SPACING, center_y=self.ACTION_HEIGHT) )

            self.actions['player2'].append(ActionSprite(action=a, action_function=self.foo,
                                                        center_x=self.parent_window.width / 2 + (idx - (size - 1) / 2)
                                                                 * self.ACTION_SPACING,
                                                        center_y=self.parent_window.height - self.ACTION_HEIGHT) )

            self.action_indeces[idx] = a

        self.player1_used = []
        self.player2_used = []


    def p1_use_action(self, act_str: str):
        self.player1_used.append(act_str)

    def p2_use_action(self, act_str: str):
        self.player2_used.append(act_str)

    def player_actions(self):
        for idx, act in enumerate(self.actions['player1']):
            yield idx, act

    def opponent_actions(self):
        for act in self.actions['player2']:
            yield act

    def get_opponent_sprite(self, index):
        return self.actions['player2'][index]

    def get_player2_sprite(self, index):
        return self.actions['player2'][index]

    def get_player1_sprite(self, index):
        return self.actions['player1'][index]

    def foo(self):
        pass

    def reset_selection(self):
        for c in self.all_actions():
            c.selected = False

    def get_selected_actions(self):
        return [act for act in self.actions['player1'] if act.selected]

    def all_actions(self):
        for k, v in self.actions.items():
            for action in v:
                yield action

    def draw(self):
        for action in self.all_actions():
            action.draw()

    def mouse_press(self, x, y):
        for card in self.actions['player1']:
            card.mouse_press(x, y)

    def mouse_release(self):
        for act in self.actions['player1']:
            if act.mouse_release():
                return 1
        return 0

    def enable_all(self):
        for i, act in self.player_actions():
            if not act.used:
                act.enabled = True

    def disable_all(self):
        for i, act in self.player_actions():
            if not act.used:
                act.enabled = False
