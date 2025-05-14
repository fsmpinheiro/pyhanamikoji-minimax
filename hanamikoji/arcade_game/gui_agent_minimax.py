from itertools import combinations
from collections import Counter
from game_tools.deck import Deck
from game_tools.scoring import evaluate_game
import random

class GUIAgentMinimax:
    def __init__(self, depth=2):
        self.turn_counter = 0
        self.search_depth = depth
        self.placed_cards = []
        self.p1_secret = []
        self.p2_placed = []
        self.p2_secret_used = False
        self.actions_remaining_p1 = ['secret', 'burn', 'gift', 'comp']

        self.action = {'secret': self.secret,
                       'burn': self.burn,
                       'gift': self.gift,
                       'comp': self.comp}



    def turn(self, cards_in_hand):
        state = {
            'p1_hand': cards_in_hand,
            'p2_hand': '',
            'p1_placed': self.placed_cards,
            'p2_placed': self.p2_placed,
            'deck': '',
            'p1_secret': self.p1_secret,
            'p2_secret': '',
            'p2_secret_used': self.p2_secret_used,
            'actions_remaining_p1': self.actions_remaining_p1.copy(),
            'actions_remaining_p2': ['secret', 'burn', 'gift', 'comp']  # pode ajustar isso depois
        }

        best_score = float('-inf')
        best_action = None
        best_selection = None

        for action in state['actions_remaining_p1']:
            selections = self.generate_card_combinations(state['p1_hand'], action)
            for cards in selections:
                new_state = self.apply_action(state.copy(), action, cards, maximizing_player=True)
                score = self.minimax(new_state, depth=self.search_depth, maximizing_player=False)
                if score > best_score:
                    best_score = score
                    best_action = action
                    best_selection = cards

        self.turn_counter += 1
        if best_action in self.action:
            self.action.pop(best_action)

        if best_action == 'gift':    # O oponente escolhe a melhor carta, as duas restantes são suas
            kept_cards = [c for c in best_selection if c != max(best_selection, key=lambda c: Deck.notation[c])]
            self.placed_cards += kept_cards
            self.p2_placed += [max(best_selection, key=lambda c: Deck.notation[c])]

        elif best_action == 'comp':
            top_two = sorted(best_selection, key=lambda c: Deck.notation[c], reverse=True)[:2]
            self.placed_cards += top_two
            self.p2_placed += [c for c in best_selection if c not in top_two]

        elif best_action == 'burn':    # A carta queimada não é registrada
            self.placed_cards += [c for c in cards_in_hand if c not in best_selection]

        elif best_action == 'secret':
            self.p1_secret = [best_selection[0]]
            self.placed_cards += [c for c in cards_in_hand if c != best_selection[0]]

        self.actions_remaining_p1.remove(best_action)
        self.turn_counter += 1

        return best_action, best_selection

    def generate_card_combinations(self, hand, action):
        if action == 'secret':
            return list(combinations(hand, 1))
        elif action == 'burn':
            return list(combinations(hand, 1))
        elif action == 'gift':
            return list(combinations(hand, 3))
        elif action == 'comp':
            return list(combinations(hand, 4))
        return []

    def apply_action(self, state, action, cards, maximizing_player):  # ação ao estado simulado
        hand_key = 'p1_hand' if maximizing_player else 'p2_hand'
        placed_key = 'p1_placed' if maximizing_player else 'p2_placed'
        secret_key = 'p1_secret' if maximizing_player else 'p2_secret'

        state[hand_key] = self.remove_cards(state[hand_key], cards)

        if action == 'secret':
            state[secret_key] = ''.join(cards)
            if not maximizing_player:
                state['p2_secret_used'] = True
        elif action == 'burn':
            pass
        elif action == 'gift':
            chosen = max(cards, key=lambda c: Deck.notation[c])
            state[placed_key] += chosen
        elif action == 'comp':
            top_two = sorted(cards, key=lambda c: Deck.notation[c], reverse=True)[:2]
            state[placed_key] += ''.join(top_two)

        return state

    def remove_cards(self, hand, cards):
        hand_list = list(hand)
        for c in cards:
            hand_list.remove(c)

        return ''.join(hand_list)

    def minimax(self, state, depth, maximizing_player):
        if depth == 0:
            return self.evaluate_state(state)

        # Gera um subconjunto aleatório de cartas possíveis
        remaining_cards = random.sample(list(Deck.notation), k=6)

        if maximizing_player:
            max_eval = float('-inf')
            for card in remaining_cards:
                new_state = state.copy()
                new_state['p1_placed'] = state['p1_placed'] + [card]
                eval = self.minimax(new_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for card in remaining_cards:
                new_state = state.copy()
                new_state['p2_placed'] = state['p2_placed'] + [card]
                eval = self.minimax(new_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_state(self, state):
        full_p1 = state['p1_placed'] + ([state['p1_secret']] if 'p1_secret' in state else [])
        if state.get('p2_secret', False):
            full_p2 = state['p2_placed']
        else:
            full_p2 = state['p2_placed']
        p1_score, p2_score, _ = evaluate_game(full_p1, full_p2, verbose=False)
        return p1_score - p2_score

    def secret(self, cards_in_hand):
        if not self.turn_counter:
            return max(cards_in_hand, key=lambda c: (Deck.notation[c], cards_in_hand.count(c) ))
        else:
            placed_counter = Counter(cards_in_hand)
            best = max(placed_counter.items(), key=lambda item: (item[1], Deck.notation[item[0] ] ))
            if best[0] in cards_in_hand:
                return best[0]
            else:
                return max(cards_in_hand, key=lambda c: (Deck.notation[c], cards_in_hand.count(c) ))

    def burn(self, cards_in_hand):
        placed_counter = Counter(self.placed_cards)
        def carta_util(c):
            return placed_counter[c], Deck.notation[c]
        return min(cards_in_hand, key=carta_util)

    def gift(self, cards_in_hand):
        return self.turn(cards_in_hand)[1]

    def comp(self, cards_in_hand):
        return self.turn(cards_in_hand)[1]

    def receive_gift(self, triplet):
        chosen = max(triplet, key=lambda c: Deck.notation[c])
        remaining = list(triplet)
        remaining.remove(chosen)
        return ''.join(remaining), chosen

    def receive_comp(self, bundles):
        sorted_cards = sorted(bundles, key=lambda c: Deck.notation[c], reverse=True)
        chosen = sorted_cards[:2]
        remaining = list(bundles)
        for c in chosen:
            remaining.remove(c)

        return ''.join(remaining), ''.join(chosen)
