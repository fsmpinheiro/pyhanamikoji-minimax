import arcade


class CardSprite(arcade.Sprite):

    cards_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets\\cards\\'

    HIGHLIGHT_COLOR = arcade.color.WHITE
    HIGHLIGHT_WIDTH = 2
    SCALE = 0.25

    def __init__(self, card: str, center_x: int, center_y: int):
        arcade.Sprite.__init__(self, filename=self.cards_path+card+'.png',
                               center_x=center_x, center_y=center_y, scale=self.SCALE)

        # These booleans control clickability, texture display and selection:
        self._enabled: bool = False
        self._flipped: bool = False
        self.pressed: bool = False
        self.selected: bool = False

        # These are the disabled and flipped textures: KEEP ORDER
        self.append_texture(arcade.load_texture(file_name=self.cards_path+card+'_disabled'+'.png', scale=self.SCALE))
        self.append_texture(arcade.load_texture(file_name=self.cards_path+'cover.png', scale=self.SCALE))

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

    HAND_HEIGHT = 150
    OFFER_HEIGHT = 250
    PLACED_HEIGHT = 400

    SPACING = 100

    def __init__(self, parent_window: arcade.Window):
        self.parent_window = parent_window

        self.cards = {'p1': [], 'p1_offer': [], 'p1_placed': [],
                      'p2': [], 'p2_offer': [], 'p2_placed': []}

        self.card_heights = {'p1': self.HAND_HEIGHT,
                             'p1_offer': self.OFFER_HEIGHT,
                             'p1_placed': self.PLACED_HEIGHT,
                             'p2': self.parent_window.height - self.HAND_HEIGHT,
                             'p2_offer': self.parent_window.height - self.OFFER_HEIGHT,
                             'p2_placed': self.parent_window.height - self.PLACED_HEIGHT}

    def reset_selection(self):
        for c in self.all_cards():
            c.selected = False

    def get_selected_cards(self, key):
        return [card for card in self.cards[key] if card.selected]

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

    def update(self, p1: str, p1_offer: str, p1_placed: str, p2: str, p2_offer: str, p2_placed: str):
        self.cards = {'p1': [], 'p1_offer': [], 'p1_placed': [],
                      'p2': [], 'p2_offer': [], 'p2_placed': []}

        for c in p1:
            self.cards['p1'].append(CardSprite(c, 0, 0))

        for c in p1_offer:
            self.cards['p1_offer'].append(CardSprite(c, 0, 0))

        for c in p1_placed:
            self.cards['p1_placed'].append(CardSprite(c, 0, 0))

        for c in p2:
            self.cards['p2'].append(CardSprite(c, 0, 0))

        for c in p2_offer:
            self.cards['p2_offer'].append(CardSprite(c, 0, 0))

        for c in p2_placed:
            self.cards['p2_placed'].append(CardSprite(c, 0, 0))

        for key, card_list in self.cards.items():
            N = len(card_list)

            for idx, card in enumerate(sorted(card_list)):
                card.set_position(center_x=self.parent_window.width / 2 + (idx - (N-1)/2) * self.SPACING,
                                  center_y=self.card_heights[key])
                card.enabled = True

    def draw(self):
        for card in self.all_cards():
            card.draw()

    def mouse_press(self, x, y):
        for c in self.all_cards():
            c.mouse_press(x, y)

    def mouse_release(self):
        for c in self.all_cards():
            c.mouse_release()
