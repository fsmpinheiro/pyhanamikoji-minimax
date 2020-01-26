import arcade
from arcade_game.cards_sprites import CardSprite


class CardTester(arcade.Window):
    def __init__(self):
        super().__init__()

        self.card_test = CardSprite('A', center_x=self.width/2, center_y=self.height/2, scale=1.0)
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


g = CardTester()
arcade.run()
