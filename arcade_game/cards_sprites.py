import arcade
from collections import defaultdict


class CardSprite(arcade.Sprite):

    cards_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets\\cards\\'

    HIGHLIGHT_COLOR = arcade.color.WHITE
    HIGHLIGHT_WIDTH = 2

    def __init__(self, card: str, center_x: int, center_y: int, scale: float = 1.0):
        arcade.Sprite.__init__(self, filename=self.cards_path+card+'.png',
                               center_x=center_x, center_y=center_y, scale=scale)

        # These booleans control clickability, texture display and selection:
        self._enabled: bool = False
        self._flipped: bool = False
        self.pressed: bool = False
        self.selected: bool = False

        # These are the disabled and flipped textures: KEEP ORDER
        self.append_texture(arcade.load_texture(file_name=self.cards_path+card+'_disabled'+'.png'))
        self.append_texture(arcade.load_texture(file_name=self.cards_path+'cover.png'))

        # Cards value:
        self.value: str = card

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

        if not self.flipped:
            self.set_texture(int(not value))

    @property
    def flipped(self):
        return self._flipped

    @flipped.setter
    def flipped(self, value: bool):
        self._flipped = value

        if self._flipped:
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

    def draw(self):
        super().draw()

        if self.selected:
            arcade.draw_lrtb_rectangle_outline(self.left, self.right, self.top, self.bottom,
                                               color=self.HIGHLIGHT_COLOR, border_width=self.HIGHLIGHT_WIDTH)

    def __lt__(self, other):
        return ord(self.value) < ord(other.value)


class CardSpriteManager:

    def __init__(self, game_window: arcade.Window):
        self.parent_window = game_window

        self.cards = {'p1': [], 'p1_offer': [], 'p1_placed': [],
                      'p2': [], 'p2_offer': [], 'p2_placed': []}

        self.card_heights = {'p1': 170, 'p1_offer': 300, 'p1_placed': 400,
                             'p2': game_window.height - 170, 'p2_offer': game_window.height - 300,
                             'p2_placed': game_window.height - 400}

    def selected_cards_in_hand(self):
        for card in self.cards['p1']:
            if card.selected:
                yield card

    def selected_cards_in_opponent_offer(self):
        for card in self.cards['p2_offer']:
            if card.selected:
                yield card

    def all_cards(self):
        for k, card_lst in self.cards.items():
            for card in card_lst:
                yield card

    card: CardSprite

    def update_locations(self):
        for key, card_list in self.cards.keys():
            N = len(card_list)

            for idx, card in enumerate(sorted(card_list)):
                card.set_position(center_x=self.parent_window.width / 2 + (idx - (N-1)/2),
                                  center_y=self.card_heights[key])

    def update(self, p1: str, p1_offer: str, p1_placed: str, p2: str, p2_offer: str, p2_placed: str):
        self.update_locations()

    def draw(self):
        for card in self.all_cards():
            card.draw()
