import itertools
import random

card_deck = 'AABBCCDDDEEEFFFFGGGGG'


def neg_intersect(big_set: tuple, small_set: tuple):
    """ This function takes two tuples: the main set and a subset and returns the negation of the intersection."""

    big_set = list(big_set)
    small_set = list(small_set)
    for s in small_set:
        if s in big_set:
            big_set.remove(s)

    return tuple(big_set)


def all_hands(deck: str, n: int):
    """ All unique combinations for a hand with n cards """

    return set(itertools.combinations(deck, n))


def get_secret_options(cards_in_hand):
    """ This function returns the set of all unique card choices the player can have with a certain hand when
    choosing the Secret action.

    """
    return set(itertools.combinations(cards_in_hand, 1))


def get_burn_options(cards_in_hand):
    """ This function returns the set of all unique card choices the player can have with a certain hand when
    choosing the Burn action.

    """
    return set(itertools.combinations(cards_in_hand, 2))


def get_gift_options(cards_in_hand):
    """ This function returns the set of all unique card choices the player can have with a certain hand when
    choosing the Gift action.

    """
    return set(itertools.combinations(cards_in_hand, 3))


def get_comp_options(cards_in_hand):

    """ This function returns the list of all possible card choices the player can have with certain cards in hand when
    choosing the Competition action.

    The output is a list of sets, where each set includes the unique card pairing for
    each choices of 4 cards from the hand.

    """

    choices_of_four = set(itertools.combinations(cards_in_hand, 4))
    all_bundling_options = []

    # For each 4 selected cards gather all possible bundling options by 2:
    for chosen_cards in choices_of_four:

        bundles = []
        divide_options = set(itertools.combinations(chosen_cards, 2))
        for div in divide_options:
            remainder = neg_intersect(chosen_cards, div)
            bundles.append(tuple(sorted((div, remainder))))

        unique_bundles = set(bundles)
        all_bundling_options.append(unique_bundles)

    return all_bundling_options


# Agent is player 1
# All possible hand combinations with 7 cards:
a = all_hands(deck=card_deck, n=7)

# Let's choose 1 random hand:
hand = random.choice(list(a))

deck_remaining = card_deck
for card in hand:
    deck_remaining = deck_remaining.replace(card, '', 1)

opponent_hands = all_hands(deck=deck_remaining, n=7)

print(f'\n Hand: {hand} and Deck remaining: {deck_remaining}')
print(f'Possible enemy hands: {len(opponent_hands)} \n')

# For each opponent hand, the opponent can choose 4 actions
N = 0

for hand in opponent_hands:
    print(f"Opponent's hand: {hand}")

    secret_options = set(itertools.combinations(hand, 1))
    print(f'Secret: {secret_options}')

    burn_options = set(itertools.combinations(hand, 2))
    print(f'Burn: {burn_options}')

    gift_options = set(itertools.combinations(hand, 3))
    print(f'Gift: {gift_options}')

    comp_options = get_comp_options(hand)
    print(f'Comp: {comp_options} \n')

    N_enemy_options = len(secret_options) + len(burn_options) + len(gift_options) + sum([len(i) for i in comp_options])

    print(f'\n Enemy options with this hand: {N_enemy_options} \n')

    N += N_enemy_options


print(f'\n \n Total Enemy options: {N}')

