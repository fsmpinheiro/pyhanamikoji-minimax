import arcade


ACTION_SPACING = 90
GEISHA_SPACING = 90


class GameWindow(arcade.Window):
    assets_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets'
    cards = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    actions = ('secret', 'burn', 'gift', 'comp')

    def __init__(self):
        super().__init__(title='Hanamikoji', antialiasing=True)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)

        self.sprites = arcade.SpriteList()
        self.texts = []

        for i in range(7):
            geisha = arcade.Sprite(self.assets_path+'\\'+self.cards[i]+'.png', scale=0.28,
                                   center_x=int(self.width/2 + (i-3) * GEISHA_SPACING), center_y=self.height/2)
            self.sprites.append(geisha)

        for i in range(4):
            asset = self.assets_path+'\\'+self.actions[i]+'.png'
            action_sprite_player = arcade.Sprite(asset, scale=0.2, center_x=int(self.width/2 + (i-1.5) * ACTION_SPACING),
                                                 center_y=60)
            action_sprite_ai = arcade.Sprite(asset, scale=0.2, center_x=int(self.width/2 + (i-1.5) * ACTION_SPACING),
                                             center_y=self.height-60)

            self.sprites.append(action_sprite_player)
            self.sprites.append(action_sprite_ai)

    def update(self, delta_time: float):
        pass

    def on_draw(self):
        arcade.start_render()

        self.sprites.draw()

        arcade.draw_text('YOU', start_x=20, start_y=30, color=arcade.color.WHITE, font_size=25)
        arcade.draw_text('AI', start_x=20, start_y=self.height-30, color=arcade.color.WHITE, font_size=25)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        print(x, y)


def main():
    gameWindow = GameWindow()
    arcade.run()
    return 0


if __name__ == '__main__':
    main()
