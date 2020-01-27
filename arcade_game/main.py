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
    GEISHA_SCALING = 0.25
    GEISHA_SPACING = 90
    BRACKET_HEIGHT = 150

    def __init__(self):
        super().__init__(title='Hanamikoji', antialiasing=True, width=1000, height=900)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)

        # Card and Agent management:
        self.deck = Deck()
        self.agent = GUIAgent()
        self.deck.pull_card()
        self.p1_cards = ''.join(self.deck.pull_card() for _ in range(7))
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
        for idx, g in enumerate(('A', 'B', 'C', 'D', 'E', 'F', 'G')):
            x = int(self.width / 2 + (idx - 3) * self.GEISHA_SPACING)
            geisha = arcade.Sprite(assets_path + 'cards\\' + g + '.png', scale=self.GEISHA_SCALING,
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

    def update_actions(self):
        if self.state == States.P1_CHOOSING:
            self.asm.reset_selection()
            self.asm.enable_all()

        elif self.state in [States.P1_SECRET,  States.P1_BURN, States.P1_GIFT, States.P1_COMP]:
            for idx, act in self.asm.player_actions():
                if idx + 3 == self.state.value:
                    act.enabled = False
                else:
                    act.enabled = True
                    act.selected = False

    def update_cards(self):
        self.csm.flip_opponent()

        if self.state in [States.P1_CHOOSING, States.P1_BURN, States.P1_GIFT, States.P1_COMP]:
            self.csm.reset_selection()
            self.csm.enable_all()

            if self.state == States.P1_CHOOSING:
                self.csm.selection_limit = 1
            elif self.state == States.P1_BURN:
                self.csm.selection_limit = 2
            elif self.state == States.P1_GIFT:
                self.csm.selection_limit = 3
            elif self.state == States.P1_COMP:
                self.csm.selection_limit = 4

    def _state_changer(f):
        """ This is a decorator for functions that change the game state. Updates all actions and cards. """

        @wraps(f)
        def wrapped(inst, *args, **kwargs):
            f(inst, *args, **kwargs)
            inst.update_actions()
            inst.update_cards()

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

        self.start_button.enabled = False
        self.start_button.visible = False

    @_state_changer
    def finish_turn_pressed(self):
        check_if_cards_correct_for_this_state = True

        if check_if_cards_correct_for_this_state:
            self.SM.to(max(self.allowed_transitions))

    @_state_changer
    def secret_pressed(self):
        if self.state == States.P1_SECRET:
            self.SM.to(States.P1_CHOOSING)
        else:
            self.SM.to(States.P1_SECRET)

    @_state_changer
    def burn_pressed(self):
        if self.state == States.P1_BURN:
            self.SM.to(States.P1_CHOOSING)
        else:
            self.SM.to(States.P1_BURN)

    @_state_changer
    def gift_pressed(self):
        if self.state == States.P1_GIFT:
            self.SM.to(States.P1_CHOOSING)
        else:
            self.SM.to(States.P1_GIFT)

    @_state_changer
    def comp_pressed(self):
        if self.state == States.P1_COMP:
            self.SM.to(States.P1_CHOOSING)
        else:
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
        if self.state != States.START:
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

        press_counter = 0

        press_counter += self.start_button.mouse_release()
        press_counter += self.asm.mouse_release()
        press_counter += self.csm.mouse_release()

        if press_counter == 0 and self.state != States.START:
            self.empty_area_pressed()


def main():
    gameWindow = Game()
    arcade.run()
    return 0


if __name__ == '__main__':
    main()
