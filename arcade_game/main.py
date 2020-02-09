import arcade
from collections import defaultdict
from game_tools.deck import Deck
from arcade_game.action_sprites import ActionSpriteManager
from arcade_game.cards_sprites import CardSpriteManager
from arcade_game.gui_agent import GUIAgent
from arcade_game.text_button import TextBoxButton
from game_tools.scoring import evaluate_game

assets_path = 'assets\\'


class Game(arcade.Window):
    GEISHA_SCALING = 0.25
    GEISHA_SPACING = 90
    BRACKET_HEIGHT = 140

    def __init__(self):
        super().__init__(title='Hanamikoji', antialiasing=True, width=1000, height=900)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)

        # Card and Agent management:
        self.deck = Deck()
        self.agent = GUIAgent()
        self.deck.pull_card()

        # Dictionary to store strings of card groups:
        self.cards = defaultdict(str)
        self.cards['p1'] = ''
        self.cards['p2'] = ''
        self.cards['p1_placed'] = ''
        self.cards['p2_placed'] = ''
        self.cards['p1_secret'] = ''
        self.cards['p2_secret'] = ''
        self.cards['offer_gift'] = ''
        self.cards['offer_comp'] = ''

        # To manage all the card and action prites:
        self.csm = CardSpriteManager(self)
        self.asm = ActionSpriteManager(self)

        # To store all static sprites:
        self.static_sprites = arcade.SpriteList()

        # Start game button 1:
        self.start_button_player = TextBoxButton(text='I start', center_x=self.width - 240, center_y=45,
                                                 width=80, height=60,
                                                 action_function=self.start_button_player_pressed)

        # Start game button 2:
        self.start_button_opponent = TextBoxButton(text='Enemy starts', center_x=self.width - 100, center_y=45,
                                                   width=140, height=60,
                                                   action_function=self.start_button_opponent_pressed)

        # Finish Turn button:
        self.finish_turn_btn = TextBoxButton(text='Finish Turn', center_x=self.width - 65, center_y=45,
                                             width=120, height=60, action_function=self.finish_button_pressed)
        self.finish_turn_btn.visible = False

        # Choosing offer button:
        self.choose_offer_btn = TextBoxButton(text='Confirm Choice', center_x=self.width - 200,
                                              center_y=self.height-210, width=150, height=60,
                                              action_function=self.choose_offer_btn_pressed)

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

        # State of the game:
        self.started = False
        self.turn_count = 0     # how many times the player has pressed the finish button
        self.did_player_start = None
        self.choosing_offer_gift = False
        self.choosing_offer_comp = False
        self.ended = False

        # Final scores:
        self.player_score = 0
        self.opponent_score = 0

    def score_game(self):

        p1_placed = self.cards['p1_placed']
        p2_placed = self.cards['p2_placed']

        p1_score, p2_score = evaluate_game(p1_cards=p1_placed, p2_cards=p2_placed)

        self.player_score = p1_score
        self.opponent_score = p2_score

    def start_button_player_pressed(self):
        self.did_player_start = True
        self.cards['p1'] = ''.join(self.deck.pull_card() for _ in range(7))
        self.cards['p2'] = ''.join(self.deck.pull_card() for _ in range(6))
        print('Your turn: CHOOSE ACTION.')
        self.start_button_pressed()

    def start_button_opponent_pressed(self):
        self.did_player_start = False
        self.cards['p1'] = ''.join(self.deck.pull_card() for _ in range(7))
        self.cards['p2'] = ''.join(self.deck.pull_card() for _ in range(6))
        self.start_button_pressed()

        self.agent_turn()

    def start_button_pressed(self):
        # Disable start buttons:
        self.start_button_player.enabled = False
        self.start_button_player.visible = False
        self.start_button_opponent.enabled = False
        self.start_button_opponent.visible = False

        # Start game:
        self.started = True

        # Update card Sprites
        self.csm.update(self.cards)
        self.csm.disable_all()

    def agent_turn(self):
        print('\n Agents turn:')
        # Pull card:
        self.cards['p2'] += self.deck.pull_card()

        # Agent select an action and cards:
        action_string, cards_selected = self.agent.turn(cards_in_hand=self.cards['p2'])

        # Manipulate card data structure:
        self.remove_from_hand_opponent(cards_to_remove=cards_selected)

        if action_string == 'secret':
            self.asm.get_opponent_sprite(index=0).used = True
            self.cards['p2_secret'] = cards_selected

        elif action_string == 'burn':
            self.asm.get_opponent_sprite(index=1).used = True

        elif action_string == 'gift':
            self.asm.get_opponent_sprite(index=2).used = True
            self.cards['offer_gift'] = cards_selected
            self.choosing_offer_gift = True
            self.asm.disable_all()

        elif action_string == 'comp':
            self.asm.get_opponent_sprite(index=3).used = True
            self.cards['offer_comp'] = cards_selected
            self.choosing_offer_comp = True
            self.asm.disable_all()

        self.csm.update(self.cards)

        print(f'>>>> Agents chose: {action_string} with cards: {cards_selected}')

    def choose_offer_btn_pressed(self):

        if self.choosing_offer_gift:
            card_sprites_selected = self.csm.get_selection(key='offer_gift')
            card_sprites_not_selected = self.csm.get_not_selection(key='offer_gift')
            valid = len(card_sprites_selected) == 1
        elif self.choosing_offer_comp:
            card_sprites_selected = self.csm.get_selection(key='offer_comp')
            card_sprites_not_selected = self.csm.get_not_selection(key='offer_comp')
            valid = len(card_sprites_selected) == 2
        else:
            card_sprites_selected = []
            card_sprites_not_selected = []
            valid = False

        if valid:
            cards_selected = ''.join(c.value for c in card_sprites_selected)
            cards_not_selected = ''.join(c.value for c in card_sprites_not_selected)

            self.cards['p1_placed'] += cards_selected
            self.cards['p2_placed'] += cards_not_selected
            self.cards['offer_gift'] = ''
            self.cards['offer_comp'] = ''
            self.choosing_offer_gift = False
            self.choosing_offer_comp = False

            self.csm.update(self.cards)

            if self.turn_count >= 4:
                self.finish_game()
            else:
                self.asm.reset_selection()
                self.asm.enable_all()
                self.csm.reset_selection()
        else:
            print('invalid offer selection')

    def remove_from_hand_player(self, cards_to_remove):
        for c in cards_to_remove:
            self.cards['p1'] = self.cards['p1'].replace(c, '', 1)

    def remove_from_hand_opponent(self, cards_to_remove):
        for c in cards_to_remove:
            self.cards['p2'] = self.cards['p2'].replace(c, '', 1)

    def finish_game(self):

        # Reveal secret cards:
        self.cards['p1_placed'] += ''.join(self.cards['p1_secret'])
        self.cards['p1_secret'] = ''

        # Reveal secret cards:
        print(self.cards['p2_secret'])
        print(self.cards['p2_placed'])

        self.cards['p2_placed'] += ''.join(self.cards['p2_secret'])
        self.cards['p2_secret'] = ''

        self.csm.update(card_dict=self.cards)
        self.finish_turn_btn.visible = False

        print(f'Game finished in state: {self.cards}')

        self.score_game()
        self.ended = True

    def finish_button_pressed(self):
        action_sprites_selected = self.asm.get_selected_actions()
        cards_selected = ''.join([c.value for c in self.csm.get_selection(key='p1')])

        # Check whether the player has chosen the correct number of actions and cards:
        selection_valid = len(action_sprites_selected) == 1 and len(cards_selected) == self.csm.selection_limit

        if not selection_valid:
            print('Invalid action / card selection')
            return

        # Execute proper action based on choice:
        action_sprite = action_sprites_selected[0]
        act = action_sprite.value
        self.remove_from_hand_player(cards_selected)

        if act == 'secret':
            self.cards['p1_secret'] = cards_selected

        elif act == 'burn':
            pass

        elif act == 'gift':
            cards_for_p1, cards_for_p2 = self.agent.receive_gift(triplet=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2

        elif act == 'comp':
            cards_for_p1, cards_for_p2 = self.agent.receive_comp(bundles=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2

        # Set the action sprite to used
        action_sprite.used = True

        # Apply next turn:
        self.turn_count += 1

        if self.did_player_start:
            self.agent_turn()
            if self.turn_count < 4:
                self.cards['p1'] += self.deck.pull_card()
            else:
                if not self.choosing_offer_gift and not self.choosing_offer_comp:
                    self.finish_game()

        elif not self.did_player_start:
            if self.turn_count < 4:
                self.agent_turn()
                self.cards['p1'] += self.deck.pull_card()
            else:
                self.finish_game()

        # Update the card sprites:
        self.csm.update(self.cards)

        # Reset everything
        self.asm.reset_selection()
        self.csm.reset_selection()
        self.csm.disable_all()

    def empty_area_pressed(self):
        """ Reset all selections and enable all buttons."""

        self.asm.reset_selection()
        self.asm.enable_all()
        self.csm.reset_selection()
        self.csm.selection_limit = 7
        self.csm.disable_all()

        # Finish turn button:
        self.finish_turn_btn.visible = False

    def secret_pressed(self):
        """ Go to secret choosing mode. 1 card limit"""

        # Action buttons:
        for idx, act in self.asm.player_actions():
            if idx == 0:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csm.reset_selection()
        self.csm.enable_all()
        self.csm.selection_limit = 1

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def burn_pressed(self):
        """ Go to secret choosing mode. 1 card limit"""

        # Action buttons:
        for idx, act in self.asm.player_actions():
            if idx == 1:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csm.reset_selection()
        self.csm.enable_all()
        self.csm.selection_limit = 2

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def gift_pressed(self):
        """ Go to gift choosing mode. 3 card limit"""

        # Action buttons:
        for idx, act in self.asm.player_actions():
            if idx == 2:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csm.reset_selection()
        self.csm.enable_all()
        self.csm.selection_limit = 3

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def comp_pressed(self):
        """ Go to secret choosing mode. 1 card limit"""

        # Action buttons:
        for idx, act in self.asm.player_actions():
            if idx == 3:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csm.reset_selection()
        self.csm.enable_all()
        self.csm.selection_limit = 4

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def on_draw(self):
        arcade.start_render()

        # Sprites:
        self.static_sprites.draw()
        arcade.draw_lines(point_list=self.line_point_list, color=arcade.color.PINK_LACE, line_width=1)

        # Buttons:
        if self.started:
            self.asm.draw()
            self.csm.draw()
        else:
            self.start_button_player.draw()
            self.start_button_opponent.draw()

        if self.choosing_offer_gift or self.choosing_offer_comp:
            self.choose_offer_btn.draw()

        if self.started and not self.choosing_offer_comp and not self.choosing_offer_gift and not self.ended:
            self.finish_turn_btn.draw()

        # Texts:
        arcade.draw_text('YOU', start_x=20, start_y=30, color=arcade.color.WHITE, font_size=20)
        arcade.draw_text('AI', start_x=20, start_y=self.height - 30, color=arcade.color.WHITE, font_size=20)

        if self.ended:
            arcade.draw_text(f'Enemy_score: {self.opponent_score}', start_x=self.width/2-200, start_y=self.height-200,
                             color=arcade.color.WHITE, font_size=50)
            arcade.draw_text(f'Your score: {self.player_score}', start_x=self.width/2-200, start_y=200,
                             color=arcade.color.WHITE, font_size=50)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

        if not self.started:
            self.start_button_player.mouse_press(x, y)
            self.start_button_opponent.mouse_press(x, y)

        if self.choosing_offer_gift or self.choosing_offer_comp:
            self.choose_offer_btn.mouse_press(x, y)
        else:
            self.finish_turn_btn.mouse_press(x, y)

        self.asm.mouse_press(x, y)
        self.csm.mouse_press(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):

        if not self.started:
            self.start_button_player.mouse_release()
            self.start_button_opponent.mouse_release()
        else:
            press_counter = 0

            if self.choosing_offer_gift or self.choosing_offer_comp:
                press_counter += self.choose_offer_btn.mouse_release()
            else:
                press_counter += self.finish_turn_btn.mouse_release()

            press_counter += self.asm.mouse_release()
            press_counter += self.csm.mouse_release()

            if press_counter == 0 and self.started:
                self.empty_area_pressed()


def main():
    Game()
    arcade.run()
    return 0


if __name__ == '__main__':
    main()
