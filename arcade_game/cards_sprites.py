import arcade


class CardSprite(arcade.Sprite):
    cards_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets\\cards\\'

    HIGHLIGHT_COLOR = arcade.color.WHITE
    HIGHLIGHT_WIDTH = 2
    SCALE = 0.25

    def __init__(self, card: str, center_x: int, center_y: int, selection_callback=None, deselection_callback=None):
        arcade.Sprite.__init__(self, filename=self.cards_path + card + '.png',
                               center_x=center_x, center_y=center_y, scale=self.SCALE)

        # These booleans control clickability, texture display and selection:
        self._enabled: bool = False
        self._flipped: bool = False
        self._selected: bool = False
        self.pressed: bool = False

        # These are the disabled and flipped textures: KEEP ORDER
        self.append_texture(
            arcade.load_texture(file_name=self.cards_path + card + '_disabled' + '.png', scale=self.SCALE))
        self.append_texture(arcade.load_texture(file_name=self.cards_path + 'cover.png', scale=self.SCALE))

        # Cards value:
        self.value: str = card

        if selection_callback is None:
            self.selection_callback = lambda: None
        else:
            self.selection_callback = selection_callback

        if deselection_callback is None:
            self.deselection_callback = lambda: None
        else:
            self.deselection_callback = deselection_callback

    def print_selected(self):
        print(f'Card selected: {self.value}')

    def print_deselected(self):
        print(f'Card deselected: {self.value}')

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

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value

        if value is True:
            self.selection_callback()
        else:
            self.deselection_callback()

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
            return True
        return False

    def draw(self):
        super().draw()

        if self.selected:
            arcade.draw_lrtb_rectangle_outline(self.left, self.right, self.top, self.bottom,
                                               color=self.HIGHLIGHT_COLOR, border_width=self.HIGHLIGHT_WIDTH)

    def __lt__(self, other):
        return ord(self.value) < ord(other.value)


class CardSpriteManager:
    HAND_HEIGHT = 170
    PLACED_HEIGHT = 340
    SECRET_HEIGHT = 350
    OFFER_HEIGHT = 200

    SPACING = 100

    def __init__(self, parent_window: arcade.Window):
        self.parent_window = parent_window

        self.cards = {'p1': [], 'p1_placed': [], 'p1_secret': [],
                      'p2': [], 'p2_placed': [], 'p2_secret': [],
                      'offer_gift': [], 'offer_comp': []}

        self.card_heights = {'p1': self.HAND_HEIGHT,
                             'p1_placed': self.PLACED_HEIGHT,
                             'p1_secret': self.SECRET_HEIGHT,
                             'p2': self.parent_window.height - self.HAND_HEIGHT,
                             'p2_placed': self.parent_window.height - self.PLACED_HEIGHT,
                             'p2_secret': self.parent_window.height - self.SECRET_HEIGHT,
                             'offer_gift': self.parent_window.height - self.OFFER_HEIGHT,
                             'offer_comp': self.parent_window.height - self.OFFER_HEIGHT}

        self.selection_limit = 7

    def check_selection_limit(self):
        N_sel = len(self.get_selection('p1'))

        if N_sel == self.selection_limit:
            for card in self.player_cards():
                if not card.selected:
                    card.enabled = False

    def flip_opponent(self):
        for c in self.opponent_cards():
            c.flipped = True

    def enable_all(self):
        for c in self.player_cards():
            c.enabled = True

    def disable_all(self):
        for c in self.player_cards():
            c.enabled = False

    def reset_selection(self):
        for c in self.all_cards():
            c.selected = False

    def get_selection(self, key):
        return [card for card in self.cards[key] if card.selected]

    def get_not_selection(self, key):
        return [card for card in self.cards[key] if not card.selected]

    def opponent_cards(self):
        for card in self.cards['p2']:
            yield card

    def player_cards(self):
        for card in self.cards['p1']:
            yield card

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

    def draw(self):
        for card in self.all_cards():
            card.draw()

    def mouse_press(self, x, y):
        for c in self.all_cards():
            c.mouse_press(x, y)

    def mouse_release(self):
        for c in self.all_cards():
            if c.mouse_release():
                return 1

        return 0

    def equal_spacing_x(self, N, idx):
        return self.parent_window.width / 2 + (idx - (N - 1) / 2) * self.SPACING

    def check_selection_gift_offer(self):
        N_sel = len(self.get_selection('offer_gift'))

        if N_sel == self.selection_limit:
            for card in self.cards['offer_gift']:
                if not card.selected:
                    card.enabled = False

        print('selecting gift offer cards now')

    def check_selection_comp_offer(self):
        N_sel = len(self.get_selection('offer_comp'))

        if N_sel == self.selection_limit:
            for card in self.cards['offer_comp']:
                if not card.selected:
                    card.enabled = False

        print('selecting comp offer cards now')

    def enable_offers(self):
        for c in self.cards['offer_gift'] + self.cards['offer_comp']:
            c.enabled = True

    def update(self, card_dict):
        self.cards = {'p1': [], 'p1_placed': [], 'p1_secret': [],
                      'p2': [], 'p2_placed': [], 'p2_secret': [],
                      'offer_gift': [], 'offer_comp': []}

        for key, card_string in card_dict.items():
            N = len(card_string)

            for idx, c in enumerate(sorted(card_string)):
                # Spawn the card:
                x = self.equal_spacing_x(N, idx)
                y = self.card_heights[key]
                card = CardSprite(c, x, y)
                card.enabled = True

                if key == 'p1':
                    card.selection_callback = self.check_selection_limit
                    card.deselection_callback = self.enable_all

                elif key == 'p1_placed':
                    pass

                elif key == 'p1_secret':
                    x = 50
                    card.set_position(x, y)
                    card.flipped = True
                    card.enabled = False

                elif key == 'p2':
                    card.flipped = True
                    card.enabled = False

                elif key == 'p2_placed':
                    pass

                elif key == 'p2_secret':
                    x = 50
                    card.set_position(x, y)
                    card.flipped = True
                    card.enabled = False

                elif key == 'offer_gift':
                    card.selection_callback = self.check_selection_gift_offer
                    card.deselection_callback = self.enable_offers

                elif key == 'offer_comp':
                    card.selection_callback = self.check_selection_comp_offer
                    card.deselection_callback = self.enable_offers

                self.cards[key].append(card)

