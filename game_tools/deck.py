from combinatoric_tools.tools import choose_from_string


class Deck:
    notation = {'A': 2,
                'B': 2,
                'C': 2,
                'D': 3,
                'E': 3,
                'F': 4,
                'G': 5}

    def __init__(self):
        self.cards = 'AABBCCDDDEEEFFFFGGGGG'

    def pull_card(self):
        card, self.cards = choose_from_string(string=self.cards, n=1)
        return card

    def __str__(self):
        return self.cards

    def __repr__(self):
        return self.cards
