import os
import arcade
from collections import defaultdict
from game_tools import Deck

from game_tools.scoring import evaluate_game
from .cards_sprites import CardSpriteManager
from .action_sprites import ActionSpriteManager
from .text_button import TextBoxButton
from .gui_agent_random import GUIAgentRandom
from .gui_agent_minimax import GUIAgentMinimax
import pprint


class Game(arcade.Window):
    CENTERCARDS_SCALING = 0.25
    CENTERCARDS_SPACING = 90
    BRACKET_HEIGHT = 110


    def __init__(self):
        super().__init__(title="Hanamikoji Python", antialiasing=True, width=1024, height=980)
        arcade.set_background_color(arcade.color.PURPLE_TAUPE)



        # atributos para usos em testes
        self.enable_print_gameplay = True
        self.rounds_left_count = 10000
        self.set_dupla_ia = True
        self.set_agent_p1 = True  # False random | True Minimax
        self.set_agent_p2 = True  # False random | True Minimax


        # Cards and Agent Management:
        self.deck = Deck()

        if self.set_agent_p2:
            self.agent_p2 = GUIAgentMinimax()
        else:
            self.agent_p2 = GUIAgentRandom()


        if self.set_dupla_ia:
            if self.set_agent_p1:
                self.agent_p1 = GUIAgentMinimax()
            else:
                self.agent_p1 = GUIAgentRandom()

        self.deck.pull_card()

        # Dictionary to store strings of card groups:
        self.cards = defaultdict(str)
        self.cards['player1'] = ''
        self.cards['player2'] = ''
        self.cards['p1_placed'] = ''
        self.cards['p2_placed'] = ''
        self.cards['p1_secret'] = ''
        self.cards['p2_secret'] = ''
        self.cards['offer_gift'] = ''
        self.cards['offer_comp'] = ''

        # To manage all the card and action sprites:
        self.csmanager = CardSpriteManager(self)
        self.asmanager = ActionSpriteManager(self)

        # To store all static sprites:
        self.static_sprites = arcade.SpriteList()

        # Start game button 1:
        self.start_button_player = TextBoxButton(text='Eu começo', center_x=self.width - 240, center_y=45,
                                                 width=120, height=60,
                                                 action_function=self.start_button_player_pressed)

        # Start game button 2:
        self.start_button_opponent = TextBoxButton(text='Oponente começa', center_x=self.width - 100, center_y=45,
                                                   width=140, height=60,
                                                   action_function=self.start_button_opponent_pressed)

        # Finish Turn button:
        self.finish_turn_btn = TextBoxButton(text='Encerrrar turno', center_x=self.width - 65, center_y=45,
                                             width=120, height=60, action_function=self.finish_turn_button_pressed)
        self.finish_turn_btn.visible = False

        # Choosing offer button:
        self.choose_offer_btn = TextBoxButton(text='Confirmar escolha', center_x=self.width - 200,
                                              center_y=self.height - 210, width=150, height=60,
                                              action_function=self.choose_offer_btn_pressed)

        # [My-Implementation] PlayAgain button:
        self.play_again_btn = TextBoxButton(text='Jogar novamente', center_x=self.width - 100, center_y=45,
                                            width=140, height=60, action_function=self.reset_game_values)
        self.play_again_btn.visible = False

        # Location of bracket lines:
        self.line_point_list = []
        self.placed_x_locations = []

        # Linhas entre cada geisha
        for i in range(8):
            x = int(self.width / 2 + (i - 3.5) * self.CENTERCARDS_SPACING)
            self.line_point_list.append([x, self.height / 2 - self.BRACKET_HEIGHT])
            self.line_point_list.append([x, self.height / 2 + self.BRACKET_HEIGHT])

        # Load Geisha sprites (geishas ao centro):
        for idx, g in enumerate(('A', 'B', 'C', 'D', 'E', 'F', 'G')):
            x = int(self.width / 2 + (idx - 3) * self.CENTERCARDS_SPACING)
            geisha = arcade.Sprite(os.path.join('assets', 'cards', g + '.png'), scale=self.CENTERCARDS_SCALING,
                                   center_x=x, center_y=self.height / 2)

            self.placed_x_locations.append(x)
            self.static_sprites.append(geisha)

        # State of the game:
        self.started = False
        self.turn_count = 0  # how many times the player has pressed the finish button
        self.did_player1_start = None
        self.did_player2_start = None
        self.choosing_offer_gift = False
        self.choosing_offer_comp = False
        self.ended = False

        # Final scores:
        self.player_score = 0
        self.opponent_score = 0




    def reset_game_values(self):
        # Resetar pontuação
        self.player_score = 0
        self.opponent_score = 0
        self.turn_count = 0
        print("Score of both players reseted\n")
        self.did_player1_start = None
        self.did_player2_start = None
        self.ended = False
        self.started = False
        self.choosing_offer_gift = False
        self.choosing_offer_comp = False
        print("Status of both players reseted")

        # Novo deck e descartar uma carta
        self.deck = Deck()
        # Resetar todas as cartas
        self.cards = defaultdict(str)
        # Atualizar sprites visuais
        self.csmanager.update(self.cards)

        # Esconder botões de gameplay
        self.finish_turn_btn.visible = False
        self.choose_offer_btn.visible = False
        self.play_again_btn.visible = False
        self.play_again_btn.enabled = False

        # Mostrar botões de escolha de início
        self.start_button_player.visible = True
        self.start_button_player.enabled = True
        self.start_button_opponent.visible = True
        self.start_button_opponent.enabled = True

        # Resetar seleções visuais
        self.asmanager.reset_selection()
        self.reset_all_actions()
        self.asmanager.enable_all()
        self.csmanager.reset_selection()
        self.csmanager.disable_all()

        # Resetar agentes
        del self.agent_p1
        del self.agent_p2
        if self.set_agent_p2:
            self.agent_p2 = GUIAgentMinimax()
        else:
            self.agent_p2 = GUIAgentRandom()

        if self.set_dupla_ia:
            if self.set_agent_p1:
                self.agent_p1 = GUIAgentMinimax()
            else:
                self.agent_p1 = GUIAgentRandom()

        # self.deck.pull_card()

    def reset_all_actions(self):
        for _, act in self.asmanager.player_actions():
            act.used = False
            act.enabled = True
            act.selected = False

        for act in self.asmanager.opponent_actions():
            act.used = False
            act.enabled = True
            act.selected = False


    def start_button_pressed(self):
        # Disable start buttons:
        self.start_button_player.enabled = False
        self.start_button_player.visible = False
        self.start_button_opponent.enabled = False
        self.start_button_opponent.visible = False

        # Start game:
        self.started = True

        # Update card Sprites
        self.csmanager.update(self.cards)
        self.csmanager.disable_all()

    def start_button_player_pressed(self):
        self.did_player1_start = True
        self.did_player2_start = False

        if(self.set_dupla_ia):          # Caso o primeiro jogador seja Agent

            self.cards['player1'] = ''.join(self.deck.pull_card() for _ in range(6))
            self.cards['player2'] = ''.join(self.deck.pull_card() for _ in range(6))
            self.start_button_pressed()     # Começa renderizar as cartas no jogo

            self.agent_p1_turn()
        else:

            self.cards['player1'] = ''.join(self.deck.pull_card() for _ in range(7))
            self.cards['player2'] = ''.join(self.deck.pull_card() for _ in range(6))  # 6
            self.start_button_pressed()

    def start_button_opponent_pressed(self):
        self.did_player1_start = False
        self.did_player2_start = True

        if(self.set_dupla_ia):

            self.cards['player1'] = ''.join(self.deck.pull_card() for _ in range(6))
            self.cards['player2'] = ''.join(self.deck.pull_card() for _ in range(6))
            self.start_button_pressed()     # Começa renderizar as cartas no jogo

            self.agent_p2_turn()
        else:

            self.cards['player1'] = ''.join(self.deck.pull_card() for _ in range(7))
            self.cards['player2'] = ''.join(self.deck.pull_card() for _ in range(6)) # 6
            self.start_button_pressed()

            self.agent_p2_turn()



    def agent_p2_turn(self):
        # Pull card:
        self.cards['player2'] += self.deck.pull_card()

        # Agent select an action and cards:
        p2_action, cards_selected = self.agent_p2.turn(cards_in_hand=self.cards['player2'])

        # Manipulate card data structure from P2 hand:
        self.remove_from_hand_opponent(cards_to_remove=cards_selected)

        if p2_action == 'secret':
            if self.enable_print_gameplay: print(f'P2 escolheu {p2_action}')

            self.asmanager.get_player2_sprite(index=0).used = True
            self.cards['p2_secret'] = cards_selected

        elif p2_action == 'burn':
            if self.enable_print_gameplay: print(f'P2 escolheu {p2_action}')

            self.asmanager.get_player2_sprite(index=1).used = True

        elif p2_action == 'gift':
            if self.enable_print_gameplay: print(f'P2 escolheu {p2_action}')

            self.asmanager.get_player2_sprite(index=2).used = True
            self.cards['offer_gift'] = cards_selected
            self.choosing_offer_gift = True
            self.asmanager.disable_all()

        elif p2_action == 'comp':
            if self.enable_print_gameplay: print(f'P2 escolheu {p2_action}')

            self.asmanager.get_player2_sprite(index=3).used = True
            self.cards['offer_comp'] = cards_selected
            self.choosing_offer_comp = True
            self.asmanager.disable_all()

        self.csmanager.update(self.cards)
        if self.set_dupla_ia:
            self.agent_p2_finish_turn(p2_action)




    def agent_p1_turn(self):
        # Pull card:
        self.cards['player1'] += self.deck.pull_card()

        # Agent select an action and cards:
        p1_action, cards_selected = self.agent_p1.turn(cards_in_hand=self.cards['player1'])

        # Manipulate card data structure from P1 hand:
        self.remove_from_hand_player(cards_to_remove=cards_selected)

        if p1_action == 'secret':
            if self.enable_print_gameplay: print(f'P1 escolheu {p1_action}')

            self.asmanager.get_player1_sprite(index=0).used = True
            self.cards['p1_secret'] = cards_selected


        elif p1_action == 'burn':
            if self.enable_print_gameplay: print(f'P1 escolheu {p1_action}')

            self.asmanager.get_player1_sprite(index=1).used = True


        elif p1_action == 'gift':
            if self.enable_print_gameplay: print(f'P1 escolheu {p1_action}')

            self.asmanager.get_player1_sprite(index=2).used = True
            self.cards['offer_gift'] = cards_selected
            self.choosing_offer_gift = True
            self.asmanager.disable_all()

        elif p1_action == 'comp':
            if self.enable_print_gameplay: print(f'P1 escolheu {p1_action}')

            self.asmanager.get_player1_sprite(index=3).used = True
            self.cards['offer_comp'] = cards_selected
            self.choosing_offer_comp = True
            self.asmanager.disable_all()

        self.csmanager.update(self.cards)
        if self.set_dupla_ia:
            self.agent_p1_finish_turn(p1_action)





    def choose_offer_btn_pressed(self):

        if self.choosing_offer_gift:
            card_sprites_selected = self.csmanager.get_selection(key='offer_gift')
            card_sprites_not_selected = self.csmanager.get_not_selection(key='offer_gift')
            valid = len(card_sprites_selected) == 1
        elif self.choosing_offer_comp:
            card_sprites_selected = self.csmanager.get_selection(key='offer_comp')
            card_sprites_not_selected = self.csmanager.get_not_selection(key='offer_comp')
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

            self.csmanager.update(self.cards)

            if self.turn_count >= 4:
                self.finish_game()
            else:
                self.asmanager.reset_selection()
                self.asmanager.enable_all()
                self.csmanager.reset_selection()
        else:
            print('invalid offer selection')

    def remove_from_hand_player(self, cards_to_remove):
        for c in cards_to_remove:
            self.cards['player1'] = self.cards['player1'].replace(c, '', 1)

    def remove_from_hand_opponent(self, cards_to_remove):
        for c in cards_to_remove:
            self.cards['player2'] = self.cards['player2'].replace(c, '', 1)


    def finish_game(self):

        # Reveal secret cards:
        self.cards['p1_placed'] += ''.join(self.cards['p1_secret'])
        self.cards['p1_secret'] = ''

        self.cards['p2_placed'] += ''.join(self.cards['p2_secret'])
        self.cards['p2_secret'] = ''

        self.csmanager.update(card_dict=self.cards)
        self.finish_turn_btn.visible = False

        print(f'Game finished in state: \n')

        pprint.pprint(self.cards)

        self.score_game()

        self.ended = True

    def score_game(self):

        p1_placed = self.cards['p1_placed']
        p2_placed = self.cards['p2_placed']

        score_difference: int

        p1_score, p2_score, score_difference = evaluate_game(p1_cards=p1_placed, p2_cards=p2_placed)

        self.player_score = p1_score
        self.opponent_score = p2_score

        # [My-Implementation]
        self.play_again_btn.enabled = True
        self.play_again_btn.visible = True

        print(f'Player Score: {self.player_score} ; Opponent Score: {self.opponent_score} ;\n '
              f'Score difference between players: {score_difference} \n')


    def agent_p1_finish_turn(self, act: str):
        if act == 'secret':
            pass
            # if self.dupla_ia and not self.did_player1_start:
            #     self.turn_count += 1

        elif act == 'burn':
            pass
            # if self.dupla_ia and not self.did_player1_start:
            #     self.turn_count += 1

        elif act == 'gift':
            cards_selected = ''.join(self.cards['offer_gift'])
            self.cards['offer_gift'] = ''
            cards_selected.join('size=1')
            cards_selected.join('replace=False')
            cards_for_p1, cards_for_p2 = self.agent_p2.receive_gift(triplet=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2
            self.choosing_offer_gift = False

            # if self.dupla_ia and not self.did_player1_start:
            #     self.turn_count += 1

        elif act == 'comp':
            cards_selected = ''.join(self.cards['offer_comp'])
            self.cards['offer_comp'] = ''
            cards_selected.join('size=2')
            cards_selected.join('replace=False')

            cards_for_p1, cards_for_p2 = self.agent_p2.receive_comp(bundles=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2
            self.choosing_offer_comp = False

            # if self.dupla_ia and not self.did_player1_start:
            #     self.turn_count += 1

        if self.set_dupla_ia and not self.did_player1_start:
            self.turn_count += 1

        if self.turn_count >= 4:
            self.finish_game()
        else:
            self.agent_p2_turn()

    def agent_p2_finish_turn(self, act: str):
        if act == 'secret':
            pass
            # if self.dupla_ia and not self.did_player2_start:
            #     self.turn_count += 1

        elif act == 'burn':
            pass
            # if self.dupla_ia and not self.did_player2_start:
            #     self.turn_count += 1


        elif act == 'gift':
            cards_selected = ''.join(self.cards['offer_gift'])
            self.cards['offer_gift'] = ''
            cards_selected.join('size=1')
            cards_selected.join('replace=False')

            cards_for_p2, cards_for_p1 = self.agent_p1.receive_gift(triplet=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2
            self.choosing_offer_gift = False

            # if self.dupla_ia and not self.did_player2_start:
            #     self.turn_count += 1


        elif act == 'comp':
            cards_selected = ''.join(self.cards['offer_comp'])
            self.cards['offer_comp'] = ''
            cards_selected.join('size=2')
            cards_selected.join('replace=False')

            cards_for_p2, cards_for_p1 = self.agent_p1.receive_comp(bundles=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2
            self.choosing_offer_comp = False

            # if self.dupla_ia and not self.did_player2_start:
            #     self.turn_count += 1


        if self.set_dupla_ia and not self.did_player2_start:
            self.turn_count += 1

        if self.turn_count >= 4:
            self.finish_game()
        else:
            self.agent_p1_turn()


    def finish_turn_button_pressed(self):
        action_sprites_selected = self.asmanager.get_selected_actions()
        cards_selected = ''.join([c.value for c in self.csmanager.get_selection(key='player1')])

        # Check whether the player has chosen the
        # correct number of actions and cards:
        selection_valid = len(action_sprites_selected) == 1 and len(cards_selected) == self.csmanager.selection_limit

        if not selection_valid:
            print('Invalid action / card selection.')
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
            cards_for_p1, cards_for_p2 = self.agent_p2.receive_gift(triplet=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2

        elif act == 'comp':
            cards_for_p1, cards_for_p2 = self.agent_p2.receive_comp(bundles=cards_selected)
            self.cards['p1_placed'] += cards_for_p1
            self.cards['p2_placed'] += cards_for_p2

        # Set the action sprite to used
        action_sprite.used = True

        # Apply next turn:
        self.turn_count += 1

        if self.did_player1_start:
            self.agent_p2_turn()
            if self.turn_count < 4:
                self.cards['player1'] += self.deck.pull_card()
            else:
                if not self.choosing_offer_gift and not self.choosing_offer_comp:
                    self.finish_game()

        elif not self.did_player1_start:
            if self.turn_count < 4:
                self.agent_p2_turn()
                self.cards['player1'] += self.deck.pull_card()
            else:
                self.finish_game()

        # Update the card sprites:
        self.csmanager.update(self.cards)

        # Reset everything
        self.asmanager.reset_selection()
        self.csmanager.reset_selection()
        self.csmanager.disable_all()

    def empty_area_pressed(self):
        """ Reset all selections and enable all buttons."""

        self.asmanager.reset_selection()
        self.asmanager.enable_all()
        self.csmanager.reset_selection()
        self.csmanager.selection_limit = 7
        self.csmanager.disable_all()

        # Finish turn button:
        self.finish_turn_btn.visible = False

    def secret_pressed(self):
        """ Go to secret choosing mode. 1 card limit"""

        # Action buttons:
        for idx, act in self.asmanager.player_actions():
            if idx == 0:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csmanager.reset_selection()
        self.csmanager.enable_all()
        self.csmanager.selection_limit = 1

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def burn_pressed(self):
        """ Go to secret choosing mode. 1 card limit"""

        # Action buttons:
        for idx, act in self.asmanager.player_actions():
            if idx == 1:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csmanager.reset_selection()
        self.csmanager.enable_all()
        self.csmanager.selection_limit = 2

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def gift_pressed(self):
        """ Go to gift choosing mode. 3 card limit"""

        # Action buttons:
        for idx, act in self.asmanager.player_actions():
            if idx == 2:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csmanager.reset_selection()
        self.csmanager.enable_all()
        self.csmanager.selection_limit = 3

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def comp_pressed(self):
        """ Go to secret choosing mode. 1 card limit"""

        # Action buttons:
        for idx, act in self.asmanager.player_actions():
            if idx == 3:
                act.selected = True
            else:
                act.selected = False

        # Card sprites:
        self.csmanager.reset_selection()
        self.csmanager.enable_all()
        self.csmanager.selection_limit = 4

        # Finish turn button:
        self.finish_turn_btn.visible = True

    def on_draw(self):
        arcade.start_render()

        # Sprites:
        self.static_sprites.draw()
        arcade.draw_lines(point_list=self.line_point_list, color=arcade.color.PINK_LACE, line_width=2)

        # Buttons:
        if self.started:
            self.asmanager.draw()
            self.csmanager.draw()
        else:
            self.start_button_player.draw()
            self.start_button_opponent.draw()


        if self.choosing_offer_gift or self.choosing_offer_comp:
            self.choose_offer_btn.draw()

        if self.started and not self.choosing_offer_comp and not self.choosing_offer_gift and not self.ended:
            self.finish_turn_btn.draw()

        # Texts:
        arcade.draw_text('Você', start_x=20, start_y=30, color=arcade.color.WHITE, font_size=20)
        arcade.draw_text('Oponente', start_x=20, start_y=self.height - 30, color=arcade.color.WHITE, font_size=20)

        if self.ended:
            self.play_again_btn.draw()

            arcade.draw_text(f'Pontos oponente: {self.opponent_score}', start_x=self.width / 2 - 200,
                             start_y=self.height - 200,color=arcade.color.WHITE, font_size=50)

            arcade.draw_text(f'Seus pontos: {self.player_score}', start_x=self.width / 2 - 200, start_y=200,
                             color=arcade.color.WHITE, font_size=50)




    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):

        if not self.started:
            self.start_button_player.mouse_press(x, y)
            self.start_button_opponent.mouse_press(x, y)

        if self.choosing_offer_gift or self.choosing_offer_comp:
            self.choose_offer_btn.mouse_press(x, y)
        else:
            self.finish_turn_btn.mouse_press(x, y)

        # on_mouse_press
        if self.ended:
            self.play_again_btn.mouse_press(x, y)

        self.asmanager.mouse_press(x, y)
        self.csmanager.mouse_press(x, y)




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

            press_counter += self.asmanager.mouse_release()
            press_counter += self.csmanager.mouse_release()

            if press_counter == 0 and self.started:
                self.empty_area_pressed()

            # on_mouse_release
            if self.ended:
                press_counter += self.play_again_btn.mouse_release()

