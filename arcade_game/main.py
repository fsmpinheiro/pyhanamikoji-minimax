import arcade
from arcade_game.gui_elements import TextBoxButton, ButtonSpriteList, ActionSprite
from game_tools.deck import Deck
from game_tools.state_machine import HanamikojiStateMachine, States

ACTION_SPACING = 90
GEISHA_SPACING = 90
GEISHA_SCALING = 0.28
CARD_SPACING = 90

assets_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets\\'
cards_path = assets_path+'\\cards\\'


class Game(arcade.Window):
    geishas = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    actions = ('secret', 'burn', 'gift', 'comp')
    cards = tuple('AABBCCDDDEEEFFFFGGGG')

    def __init__(self):
        super().__init__(title='Hanamikoji', antialiasing=True)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)

        # To store all sprites:
        self.static_sprites = arcade.SpriteList()
        self.card_sprites = arcade.SpriteList()
        self.action_sprites = ButtonSpriteList()

        self.action_functions = [self.secret, self.burn, self.gift, self.comp]

        # One time button at the start of the game:
        self.start_button = TextBoxButton(text='Start Game', center_x=self.width-65, center_y=45,
                                          width=120, height=60, action_function=self.start_game)

        # Load Geisha sprites:
        [self.static_sprites.append(arcade.Sprite(assets_path+self.geishas[i]+'.png', scale=GEISHA_SCALING,
                                                  center_x=int(self.width/2 + (i-3) * GEISHA_SPACING),
                                                  center_y=self.height/2)) for i in range(7)]

        # Game logic:
        self.SM = HanamikojiStateMachine()

        self.deck = Deck()
        self.player_cards = ''
        self.opponent_cards = ''
        self.discarded_cards = ''
        self.player_placed_cards = ''
        self.opponent_placed_cards = ''

        self.started = False

    @property
    def state(self):
        return self.SM.state

    def start_game(self):
        print('Started game')
        self.SM.to(States.P1_CHOOSING)

        # GUI ACTIONS:
        self.started = True
        self.start_button.disable()
        for idx, action in enumerate(self.actions):
            action_player = ActionSprite(filename=assets_path+action+'.png', scale=0.2,
                                         center_x=int(self.width/1.5 + (idx-3) * ACTION_SPACING),
                                         center_y=60,
                                         action_function=self.action_functions[idx])

            action_opponent = ActionSprite(filename=assets_path+action+'.png', scale=0.2,
                                           center_x=int(self.width/1.5 + (idx-3) * ACTION_SPACING),
                                           center_y=self.height-60,
                                           action_function=self.action_functions[idx])
            action_opponent.disable()

            self.action_sprites.append(action_player)
            self.action_sprites.append(action_opponent)

        # GAME LOGIC:
        self.deck.pull_card()
        self.player_cards = ''.join([self.deck.pull_card() for _ in range(6)])
        self.opponent_cards = ''.join([self.deck.pull_card() for _ in range(6)])

        print(f'Player cards: {self.player_cards}')
        print(f'Opponent cards: {self.opponent_cards}')

    def secret(self):
        self.SM.to(States.P1_SECRET)
        print(self.state)

    def burn(self):
        self.SM.to(States.P1_BURN)
        print(self.state)

    def gift(self):
        self.SM.to(States.P1_GIFT)
        print(self.state)

    def comp(self):
        self.SM.to(States.P1_COMP)
        print(self.state)

    def on_draw(self):
        arcade.start_render()

        self.static_sprites.draw()
        self.card_sprites.draw()
        self.action_sprites.draw()

        if self.state == States.START:
            self.start_button.draw()

        arcade.draw_text('YOU', start_x=20, start_y=30, color=arcade.color.WHITE, font_size=20)
        arcade.draw_text('AI', start_x=20, start_y=self.height-30, color=arcade.color.WHITE, font_size=20)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.start_button.check_mouse_press(x, y):
            self.start_button.on_press()

        self.action_sprites.check_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.start_button.pressed:
            self.start_button.on_release()

        if self.action_sprites.check_release() == 0:
            self.SM.to(States.P1_CHOOSING)


def main():
    gameWindow = Game()
    arcade.run()
    return 0


if __name__ == '__main__':
    main()
