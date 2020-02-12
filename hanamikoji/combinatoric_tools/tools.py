import random
import itertools


def join_tuples(h, g):
    return tuple(''.join(h) + ''.join(g))


def flatten(x):
    output = []

    def flatten_tuple(t):
        for i in t:
            if type(i) == tuple:
                flatten_tuple(i)
            else:
                output.append(i)

    flatten_tuple(x)
    return tuple(output)


def choose_from_string(string: str, n: int):
    """ Choose a card from a string. Returns the choice and what remains after choosing. """

    assert len(string) >= n
    choices = []
    for _ in range(n):
        char = random.choice(string)
        string = string.replace(char, '', 1)

        choices.append(char)

    return ''.join(choices), string


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
    return tuple(set(itertools.combinations(cards_in_hand, 1)))


def get_burn_options(cards_in_hand):
    """ This function returns the set of all unique card choices the player can have with a certain hand when
    choosing the Burn action.

    """
    return tuple(set(itertools.combinations(cards_in_hand, 2)))


def get_gift_options(cards_in_hand):
    """ This function returns the set of all unique card choices the player can have with a certain hand when
    choosing the Gift action.

    """
    return tuple(set(itertools.combinations(cards_in_hand, 3)))


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

        unique_bundles = tuple(set(bundles))
        all_bundling_options.append(unique_bundles)

    options_unwrapped = []
    for i in all_bundling_options:
        for j in i:
            options_unwrapped.append(j)

    return tuple(options_unwrapped)
