import random
from deck import choose_from_string


class RandomAgent:
    def __init__(self, name='Agent __'):
        self.name = name
        self.hand = ''
        self.cards_placed = []

        self.actions = {'secret': self.secret,
                        'burn': self.burn,
                        'gift': self.gift,
                        'comp': self.comp}

    def secret(self, opponent):
        card_chosen, self.hand = choose_from_string(string=self.hand, n=1)
        self.cards_placed += card_chosen

        return card_chosen

    def burn(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=2)

        return cards_chosen

    def gift(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=3)
        self.cards_placed += opponent.receive_gift(cards_chosen)

        return cards_chosen

    def comp(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=4)
        bundle_1, bundle_2 = choose_from_string(cards_chosen, n=2)
        self.cards_placed += opponent.receive_comp([bundle_1, bundle_2])

        return (bundle_1, bundle_2)

    def receive_gift(self, triplet):
        card_chosen, cards_discarded = choose_from_string(triplet, 1)
        self.cards_placed += card_chosen

        return cards_discarded

    def receive_comp(self, bundles):
        ch_idx = random.choice([0, 1])
        if ch_idx == 0:
            self.cards_placed += bundles[0]
            return bundles[1]
        else:
            self.cards_placed += bundles[1]
            return bundles[0]

    def status(self):
        self.hand = ''.join(sorted(self.hand))
        self.cards_placed = ''.join(sorted(self.cards_placed))
        print(f'{self.name}: with hand: {self.hand} and cards placed: {self.cards_placed}')

    def turn(self, deck, opponent):
        self.hand += deck.pull_card()
        print(f'{self.name} has these cards: {self.hand}')

        # Choose the action randomly for now:
        action_key = random.choice(list(self.actions.keys()))

        # Do the action:
        cards_played = self.actions[action_key](opponent=opponent)
        print(f'{self.name} has chosen {action_key} with cards: {cards_played}')

        # Remove the action from the options:
        self.actions.pop(action_key)

        # Tell the opponent what we just did:
        opponent.opponent_actions.pop(action_key)
