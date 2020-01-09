import deck
import numpy as np
import itertools


class Agent:
    def __init__(self, name):

        # All possible action permutations:
        self.perm = list(itertools.permutations([self.secret, self.burn, self.gift, self.comp]))

        # Start with an equal chance to choose all
        self.genes = np.ones(len(self.perm))/len(self.perm)

        # Choose the order of actions:
        perm_idx = np.random.choice(range(24), p=self.genes)
        self.choice = self.perm[perm_idx]

        # Keeping track of game state:
        self.cards = []
        self.cards_placed = []

        # This is for printing
        self.name = name

    def pull_card(self, deck):
        self.cards.append(deck.pull_card())

    def turn(self, turn_index, opponent):
        self.choice[turn_index](opponent)

    def secret(self, opponent):
        card = np.random.choice(self.cards)
        print(f'{self.name}: Chose Secret with card: {card}')

        self.cards.remove(card)
        self.cards_placed.append(card)

    def burn(self, opponent):
        cards = np.random.choice(self.cards, size=2, replace=False)
        print(f'{self.name}: Chose Burn with cards: {cards}')

        [self.cards.remove(c) for c in cards]

    def gift(self, opponent):
        cards = np.random.choice(self.cards, size=3, replace=False)
        print(f'{self.name}: Chose Gift with cards: {cards}')

        [self.cards.remove(c) for c in cards]
        cards_not_taken = opponent.get_gift(cards)

        [self.cards_placed.append(c) for c in cards_not_taken]

    def comp(self, opponent):
        cards = np.random.choice(self.cards, size=4, replace=False)
        print(f'{self.name}: Chose comp with cards: {cards[:2]} and {cards[2:]}')

        [self.cards.remove(c) for c in cards]
        cards_not_taken = opponent.get_comp(cards[:2], cards[2:])

        [self.cards_placed.append(c) for c in cards_not_taken]

    def get_gift(self, cards):
        choice = np.random.choice(cards)
        print(f'{self.name}: Chose this card and placed it: {choice}')

        self.cards_placed.append(choice)

        cards = list(cards)
        cards.remove(choice)

        return cards

    def get_comp(self, cards_left, cards_right):
        ch_idx = np.random.choice([0, 1])
        if ch_idx == 0:
            choice = cards_left
        else:
            choice = cards_right

        print(f'{self.name}: Chose these cards and placed them: {choice}')

        [self.cards_placed.append(c) for c in choice]

        return list(cards_right) if ch_idx == 0 else list(cards_left)


p1 = Agent(name='Player 1')
p2 = Agent(name='Player 2')
d = deck.Deck()

# Pull random card out.
d.pull_card()
p1.cards = [d.pull_card() for _ in range(6)]
p2.cards = [d.pull_card() for _ in range(6)]

# Turns:
for i in range(4):
    p1.pull_card(deck=d)
    print(p1.cards)
    p1.turn(turn_index=i, opponent=p2)

    p2.pull_card(deck=d)
    print(p2.cards)
    p2.turn(turn_index=i, opponent=p1)

print(p1.cards_placed)
print(p2.cards_placed)
