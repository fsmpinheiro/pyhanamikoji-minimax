from functools import wraps
import arcade
from arcade_game.action_sprites import ActionSpriteManager
from arcade_game.cards_sprites import CardSpriteManager
from arcade_game.gui_agent import GUIAgent
from arcade_game.text_button import TextBoxButton
from game_tools.deck import Deck
from game_tools.state_machine import HanamikojiStateMachine, States

assets_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets\\'


# noinspection PyCallingNonCallable,PyMethodParameters,PyArgumentList
class Game(arcade.Window):
    ACTION_SCALING = 0.2
    ACTION_SPACING = 110
    ACTION_HEIGHT = 50

    GEISHA_SCALING = 0.25
    GEISHA_SPACING = 90

    CARD_SCALING = 0.25
    CARD_SPACING = 100
    CARD_HEIGHT = 170

    BRACKET_HEIGHT = 150

    geishas = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    def __init__(self):
        super().__init__(title='Hanamikoji', antialiasing=True, width=1000, height=900)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)

        # Card and Agent management:
        self.deck = Deck()
        self.agent = GUIAgent()
        self.deck.pull_card()
        self.p1_cards = ''.join(self.deck.pull_card() for _ in range(6))
        self.p2_cards = ''.join(self.deck.pull_card() for _ in range(6))

        # To store all the cards sprites:
        self.csm = CardSpriteManager(self)

        # To store all the action sprites:
        self.asm = ActionSpriteManager(self)

        # To store all static sprites:
        self.static_sprites = arcade.SpriteList()

        # Start game button:
        self.start_button = TextBoxButton(text='Start Game', center_x=self.width - 65, center_y=45,
                                          width=120, height=60, action_function=self.start_button_pressed)

        # Finish Turn button:
        self.finish_turn_btn = TextBoxButton(text='Finish Turn', center_x=self.width - 65, center_y=45,
                                             width=120, height=60, action_function=self.finish_turn_pressed)

        # Location of bracket lines:
        self.line_point_list = []
        self.placed_x_locations = []
        for i in range(8):
            x = int(self.width/2 + (i - 3.5) * self.GEISHA_SPACING)
            self.line_point_list.append([x, self.height/2-self.BRACKET_HEIGHT])
            self.line_point_list.append([x, self.height/2+self.BRACKET_HEIGHT])

        # Load Geisha sprites:
        for i in range(7):
            x = int(self.width / 2 + (i - 3) * self.GEISHA_SPACING)
            geisha = arcade.Sprite(assets_path + 'cards\\' + self.geishas[i] + '.png', scale=self.GEISHA_SCALING,
                                                  center_x=x, center_y=self.height / 2)
            self.placed_x_locations.append(x)
            self.static_sprites.append(geisha)

        # GUI logic with the GAME:
        self.SM = HanamikojiStateMachine()

    @property
    def state(self):
        return self.SM.state

    @property
    def allowed_transitions(self):
        return self.SM.get_allowed_transitions()

    def update_buttons(self):
        pass

    def _state_changer(f):
        """ This is a decorator for functions that change the game state. Updates all buttons. """

        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            f(inst, *args, **kwargs)
            inst.update_buttons()

        return wrapped

    def _card_changer(f):
        """ This is a decorator for functions that change the list of cards. Updates all buttons. """

        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            f(inst, *args, **kwargs)
            inst.csm.update(inst.p1_cards, '', '', inst.p2_cards, '', '')

        return wrapped

    @_state_changer
    @_card_changer
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
        arcade.draw_lines(point_list=self.line_point_list, color=arcade.color.PINK_LACE, line_width=1)

        # Buttons:
        self.asm.draw()
        self.csm.draw()
        self.start_button.draw()

        # Texts:
        arcade.draw_text('YOU', start_x=20, start_y=30, color=arcade.color.WHITE, font_size=20)
        arcade.draw_text('AI', start_x=20, start_y=self.height - 30, color=arcade.color.WHITE, font_size=20)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

        self.start_button.mouse_press(x, y)
        self.asm.mouse_press(x, y)
        self.csm.mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):

        self.start_button.mouse_release()
        self.asm.mouse_release()
        self.csm.mouse_release()


def main():
    gameWindow = Game()
    arcade.run()
    return 0


if __name__ == '__main__':
    main()
