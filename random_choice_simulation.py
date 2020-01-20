from deck import *
import random


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


# Init objects:
d = Deck()
P1 = Agent(name='Player_1')
P2 = Agent(name='Player_2')

# Deal cards:
d.pull_card()
P1.hand = ''.join([d.pull_card() for _ in range(6)])
P2.hand = ''.join([d.pull_card() for _ in range(6)])

# Turns:
for i in range(4):
    P1.turn(deck=d, opponent=P2)

    P2.turn(deck=d, opponent=P1)

P1.status()

P2.status()


def evaluate_game(p1_placed, p2_placed):

    p1_points = 0
    p2_points = 0

    p1_geishas = 0
    p2_geishas = 0

    for key, value in Deck.notation.items():
        p1 = p1_placed.count(key)
        p2 = p2_placed.count(key)

        if p1 > p2:
            print(f'For card: {key}: Player 1 has won {value} points.')
            p1_points += value
            p1_geishas += 1
        elif p1 < p2:
            print(f'For card: {key}: Player 2 has won {value} points.')
            p2_points += value
            p2_geishas += 1
        else:
            print(f'For card: {key}: draw, no points are given')

    if p1_points >= 11 or p1_geishas >= 4:
        winner = 'Player 1'
    elif p2_points  >= 11 or p2_geishas >= 4:
        winner = 'Player 2'
    else:
        winner = 'No one.'

    print(f'\n SUMMARY: \n '
          f'>>>> Player 1 has {p1_points} with {p1_geishas} Geishas. \n'
          f' >>>> Player 2 has {p2_points} with {p2_geishas} Geishas. \n'
          f' >>>> >>>> {winner} has won!')


evaluate_game(P1.cards_placed, P2.cards_placed)
