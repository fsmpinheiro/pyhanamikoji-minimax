import itertools


# The amount of choices the agent has for a given set of cards in the agent's hand:

def secret(cards_in_hand):
    """ Secret: choose one unique card and hide it. """
    return len(set(itertools.combinations(cards_in_hand, 1)))


def burn(cards_in_hand):
    """ Burn: choose a unique set of two cards and discard them. """
    return len(set(itertools.combinations(cards_in_hand, 2)))


def gift(cards_in_hand):
    """ Gift: choose a unique set of three cards and offer them to the opponent. """
    return len(set(itertools.combinations(cards_in_hand, 3)))


def comp(cards_in_hand):
    """ Competition: choose a unique set of four cards, divide them into two groups of two and offer them to the
    opponent. """
    choose_4 = set(itertools.combinations(cards_in_hand, 4))

    number_of_options = 0
    for i in choose_4:
        divide_options = len(set(itertools.combinations(i, 2)))
        if divide_options == 1:
            number_of_options += 1
        else:
            number_of_options += divide_options // 2

    return number_of_options


# The four actions that can be chosen from:
actions = [secret, burn, gift, comp]

# All the permutations of these actions: (done using the indeces)
action_index_permutations = set(itertools.permutations([0, 1, 2, 3]))

# The card deck setup:
card_deck = 'AABBCCDDDEEEFFFFGGGGG'


# All unique combinations for a hand with n cards:
def all_hands(n):
    return set(itertools.combinations(card_deck, n))


# Integer used for counting all options:
N_total = 0

# Loop through all possible action permutation choices:
for action_permutation in action_index_permutations:

    # We start with 7 cards
    N_cards = 7

    # Loop through each action:
    for action_index in action_permutation:

        # All possible cards in the agent's hand with N cards:
        all_possible_hands = all_hands(N_cards)

        # For each hand gather all unique options we have:
        for hand in all_possible_hands:
            N_options = actions[action_index](hand)
            N_total += N_options

        # In the next turn we have a different number of cards depending on the action index.
        N_cards += -action_index

print(N_total)
