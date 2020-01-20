import random


def choose_from_string(string: str, n: int):
    assert len(string) >= n
    choices = []
    for _ in range(n):
        char = random.choice(string)
        string = string.replace(char, '', 1)

        choices.append(char)

    return ''.join(choices), string


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
        # Pull a random card:
        # card = random.choice(self.cards)

        # Delete it from the deck:
        # self.cards = self.cards.replace(card, '', 1)

        card, self.cards = choose_from_string(string=self.cards, n=1)

        return card

    def __str__(self):
        return self.cards

    def __repr__(self):
        return self.cards
