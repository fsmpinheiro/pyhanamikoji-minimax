import arcade

from arcade_game.action_sprites import ActionSpriteManager
from arcade_game.cards_sprites import CardSprite, CardSpriteManager


class CardTester(arcade.Window):
    def __init__(self):
        super().__init__()

        self.card_test = CardSprite('A', center_x=self.width/2, center_y=self.height/2)
        self.card_test.enabled = True

    def on_draw(self):
        arcade.start_render()
        self.card_test.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.card_test.mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.card_test.mouse_release()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.card_test.enabled = not self.card_test.enabled

        elif symbol == arcade.key.F:
            self.card_test.flipped = not self.card_test.flipped


class CardManagerTester(arcade.Window):
    def __init__(self):
        super().__init__(height=900)
        self.csm = CardSpriteManager(parent_window=self)

    def on_draw(self):
        arcade.start_render()
        self.csm.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.csm.mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.csm.mouse_release()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            try:
                self.csm.update('A', 'BB', 'CCC', 'BBBB', 'DDDDD', 'EEEEEE')
            except Exception as e:
                print(e)
        elif symbol == arcade.key.F:
            self.csm.update('AF', '', '', 'BB', '', 'D')
        elif symbol == arcade.key.G:
            self.csm.update('AAFGB', '', '', 'BGGC', '', 'D')

        elif symbol == arcade.key.S:
            print(self.csm.get_selected_cards(key='p2_offer'))

        elif symbol == arcade.key.R:
            self.csm.reset_selection()


class ActionManagerTester(arcade.Window):
    def __init__(self):
        super().__init__(height=900)
        self.asm = ActionSpriteManager(parent_window=self)

    def on_draw(self):
        arcade.start_render()
        self.asm.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.asm.mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.asm.mouse_release()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.G:
            for act in self.asm.all_actions():
                act.used = True

        elif symbol == arcade.key.S:
            print(self.asm.get_selected_actions())


g = ActionManagerTester()
arcade.run()
