from collections import defaultdict
from functools import wraps
import arcade
from arcade_game.gui_elements import TextBoxButton, ActionSpriteList, ActionSprite
from game_tools.deck import Deck
from game_tools.state_machine import HanamikojiStateMachine, States

assets_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets\\'
cards_path = assets_path + '\\cards\\'


# noinspection PyCallingNonCallable,PyMethodParameters,PyArgumentList
class Game(arcade.Window):
    ACTION_SPACING = 90
    GEISHA_SPACING = 90
    GEISHA_SCALING = 0.28
    CARD_SPACING = 90

    geishas = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    def __init__(self):
        super().__init__(title='Hanamikoji', antialiasing=True, resizable=True)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)

        # To store all sprites:
        self.static_sprites = arcade.SpriteList()
        self.action_sprites_player = ActionSpriteList(assets_path=assets_path, game_window=self)
        self.action_sprites_opponent = ActionSpriteList(assets_path=assets_path, game_window=self, opponent=True)

        # Start game button:
        self.start_button = TextBoxButton(text='Start Game', center_x=self.width - 65, center_y=45,
                                          width=120, height=60, action_function=self.start_button_pressed)

        # Finish Turn button:
        self.finish_turn_btn = TextBoxButton(text='Finish Turn', center_x=self.width - 65, center_y=45,
                                             width=120, height=60, action_function=self.finish_turn_pressed)

        # Load Geisha sprites:
        [self.static_sprites.append(arcade.Sprite(assets_path + self.geishas[i] + '.png', scale=self.GEISHA_SCALING,
                                                  center_x=int(self.width / 2 + (i - 3) * self.GEISHA_SPACING),
                                                  center_y=self.height / 2)) for i in range(7)]

        # Game logic:
        self.SM = HanamikojiStateMachine()

        self.enabled_buttons_dict = defaultdict(list)

        for s in States:
            if s == States.START:
                self.enabled_buttons_dict[s] = [self.start_button]
            elif s == States.P1_CHOOSING:
                self.enabled_buttons_dict[s] = self.action_sprites_player.available()
            elif s.is_p1_choosing_cards():
                self.enabled_buttons_dict[s] = self.action_sprites_player.other_than(state=s) + [self.finish_turn_btn]

            self.enabled_buttons_dict[s] += self.action_sprites_opponent.available()

        self.visible_buttons_dict = defaultdict(list)
        for s in States:
            if s == States.START:
                self.visible_buttons_dict[s] = [self.start_button]
            elif s.is_p1_choosing_cards():
                self.visible_buttons_dict[s] += self.action_sprites_player.all() + self.action_sprites_opponent.all() \
                                                + [self.finish_turn_btn]
            else:
                self.visible_buttons_dict[s] += self.action_sprites_player.all() + self.action_sprites_opponent.all()

        self.update_buttons()

        # Card management:


    @property
    def state(self):
        return self.SM.state

    @property
    def allowed_transitions(self):
        return self.SM.get_allowed_transitions()

    @property
    def enabled_buttons(self):
        return self.enabled_buttons_dict[self.state]

    @property
    def visible_buttons(self):
        return self.visible_buttons_dict[self.state]

    def get_all_buttons(self):
        return [self.start_button, self.finish_turn_btn] + self.action_sprites_player.all()

    def update_buttons(self):

        for btn in self.get_all_buttons():
            btn.set_enabled(False)
            btn.set_visible(False)

        for btn in self.enabled_buttons:
            btn.set_enabled(True)

        for btn in self.visible_buttons:
            btn.set_visible(True)

    def _state_changer(f):
        """ This is a decorator for functions that change the game state. Updates all buttons. """

        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            f(inst, *args, **kwargs)
            inst.update_buttons()

        return wrapped

    @_state_changer
    def start_button_pressed(self):
        self.SM.to(States.P1_CHOOSING)

    @_state_changer
    def finish_turn_pressed(self):
        check_if_cards_correct_for_this_state = True

        if check_if_cards_correct_for_this_state:
            self.SM.to(max(self.allowed_transitions))

    @_state_changer
    def secret_pressed(self):
        self.SM.to(States.P1_SECRET)

    @_state_changer
    def burn_pressed(self):
        self.SM.to(States.P1_BURN)

    @_state_changer
    def gift_pressed(self):
        self.SM.to(States.P1_GIFT)

    @_state_changer
    def comp_pressed(self):
        self.SM.to(States.P1_COMP)

    @_state_changer
    def empty_area_pressed(self):
        self.SM.to(States.P1_CHOOSING)

    def on_draw(self):
        arcade.start_render()

        # Sprites:
        self.static_sprites.draw()

        # Buttons:
        [sp.draw() for sp in self.get_all_buttons()]
        [sp.draw() for sp in self.action_sprites_opponent.btn_lst]

        # Texts:
        arcade.draw_text('YOU', start_x=20, start_y=30, color=arcade.color.WHITE, font_size=20)
        arcade.draw_text('AI', start_x=20, start_y=self.height - 30, color=arcade.color.WHITE, font_size=20)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.start_button.check_mouse_press(x, y):
            self.start_button.on_press()

        if self.finish_turn_btn.check_mouse_press(x, y):
            self.finish_turn_btn.on_press()

        self.action_sprites_player.check_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pressed_count = 0
        for sp in self.get_all_buttons():
            if sp.pressed:
                pressed_count += 1
                sp.on_release()

        if pressed_count == 0:
            self.empty_area_pressed()


def main():
    gameWindow = Game()
    arcade.run()
    return 0


if __name__ == '__main__':
    main()
