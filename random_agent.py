import random
from deck import choose_from_string


class Agent:
    def __init__(self, name='Agent __'):
        self.name = name
        self.hand = ''
        self.actions = [self.secret, self.burn, self.gift, self.comp]
        self.cards_placed = ''

    def secret(self, opponent):
        card_chosen, self.hand = choose_from_string(string=self.hand, n=1)
        self.cards_placed += card_chosen

    def burn(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=2)

    def gift(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=3)
        self.cards_placed += opponent.get_gift(cards_chosen)

    def comp(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=4)
        bundle_1, bundle_2 = choose_from_string(cards_chosen, n=2)
        self.cards_placed += opponent.get_comp([bundle_1, bundle_2])

    def get_gift(self, triplet):
        card_chosen, cards_discarded = choose_from_string(triplet, 1)
        self.cards_placed += card_chosen
        return cards_discarded

    def get_comp(self, bundles):
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

        action = random.choice(self.actions)
        self.actions.remove(action)

        action(opponent=opponent)
