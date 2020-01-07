import random


class Deck:
    def __init__(self):
        self.deck_setup = {'red': 2,
                           'purple': 2,
                           'yellow': 2,
                           'blue': 3,
                           'orange': 3,
                           'green': 4,
                           'pink': 5}

        self.cards = []
        for i, j in self.deck_setup.items():
            for _ in range(j):
                card = {'color': i,
                        'number': j}

                self.cards.append(card)

    def pull_card(self):
        try:
            card = random.choice(self.cards)
        except IndexError:
            print('No more cards in this deck. Deleting self.')
            del self
            return None

        self.cards.remove(card)
        return card
