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
        super().__init__(title='Hanamikoji', antialiasing=True)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)

        # To store all sprites:
        self.static_sprites = arcade.SpriteList()
        self.action_sprites_player = ActionSpriteList(assets_path=assets_path, game_window=self)
        self.action_sprites_opponent = ActionSpriteList(assets_path=assets_path, game_window=self, opponent=True)

        # Start game button:
        self.start_button = TextBoxButton(text='Start Game', center_x=self.width - 65, center_y=45,
                                          width=120, height=60, action_function=self.start_button_pressed)

        # Load Geisha sprites:
        [self.static_sprites.append(arcade.Sprite(assets_path + self.geishas[i] + '.png', scale=self.GEISHA_SCALING,
                                                  center_x=int(self.width / 2 + (i - 3) * self.GEISHA_SPACING),
                                                  center_y=self.height / 2)) for i in range(7)]

        # Game logic:
        self.SM = HanamikojiStateMachine()

        self.enabled_buttons_dict = {s: [] for s in States}
        self.enabled_buttons_dict = {**self.enabled_buttons_dict,
                                     States.START: [self.start_button],
                                     States.P1_CHOOSING: self.action_sprites_player.available,

                                     States.P1_SECRET: self.action_sprites_player.not_secret(),
                                     States.P1_BURN: self.action_sprites_player.not_burn(),
                                     States.P1_GIFT: self.action_sprites_player.not_gift(),
                                     States.P1_COMP: self.action_sprites_player.not_comp()}

        self.visible_buttons_dict = {s: [] for s in States}
        self.visible_buttons_dict = {**self.visible_buttons_dict,
                                     States.START: [self.start_button],
                                     States.P1_CHOOSING: self.action_sprites_player.all(),
                                     States.P1_SECRET: self.action_sprites_player.all(),
                                     States.P1_BURN: self.action_sprites_player.all(),
                                     States.P1_GIFT: self.action_sprites_player.all(),
                                     States.P1_COMP: self.action_sprites_player.all()}

    @property
    def state(self):
        return self.SM.state

    def get_all_buttons(self):
        return [self.start_button] + self.action_sprites_player.all()

    @property
    def enabled_buttons(self):
        return self.enabled_buttons_dict[self.state]

    @property
    def visible_buttons(self):
        return self.visible_buttons_dict[self.state]

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

        self.static_sprites.draw()
        self.action_sprites_player.draw()
        self.action_sprites_opponent.draw()
        self.start_button.draw()

        arcade.draw_text('YOU', start_x=20, start_y=30, color=arcade.color.WHITE, font_size=20)
        arcade.draw_text('AI', start_x=20, start_y=self.height - 30, color=arcade.color.WHITE, font_size=20)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.start_button.check_mouse_press(x, y):
            self.start_button.on_press()

        self.action_sprites_player.check_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.start_button.pressed:
            self.start_button.on_release()

        if self.action_sprites_player.check_release() == 0:
            self.empty_area_pressed()


def main():
    gameWindow = Game()
    arcade.run()
    return 0


if __name__ == '__main__':
    main()
