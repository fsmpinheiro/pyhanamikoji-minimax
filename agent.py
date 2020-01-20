import itertools
import random
card_deck = 'AABBCCDDDEEEFFFFGGGGG'


def choose_from_string(string: str, n: int):
    """ Choose a card from a string"""
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


class Agent:
    def __init__(self, name='Agent __'):
        self.name = name
        self.hand = ''
        self.cards_placed = []

        self.actions = {'secret': self.secret,
                        'burn': self.burn,
                        'gift': self.gift,
                        'comp': self.comp}

        self.option_counters = {'secret': get_secret_options,
                                'burn': get_burn_options,
                                'gift': get_gift_options,
                                'comp': get_comp_options}

        self.opponent_actions = {'secret': self.secret,
                                 'burn': self.burn,
                                 'gift': self.gift,
                                 'comp': self.comp}

    def secret(self, opponent):
        card_chosen, self.hand = choose_from_string(string=self.hand, n=1)
        self.cards_placed += card_chosen

    def burn(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=2)

    def gift(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=3)
        self.cards_placed += opponent.receive_gift(cards_chosen)

    def comp(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=4)
        bundle_1, bundle_2 = choose_from_string(cards_chosen, n=2)
        self.cards_placed += opponent.receive_comp([bundle_1, bundle_2])

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

        # Calculate the options this agent has for this turn:
        self.own_options()

        # Calculate enemy options:
        deck_remaining = card_deck
        for card in self.hand:
            deck_remaining = deck_remaining.replace(card, '', 1)

        for card in self.cards_placed:
            deck_remaining = deck_remaining.replace(card, '', 1)

        for card in opponent.cards_placed:
            deck_remaining = deck_remaining.replace(card, '', 1)

        opponent_hands = all_hands(deck=deck_remaining, n=len(opponent.hand)+1)

        print(f'Possible opponent hands: {len(opponent_hands)} \n\n')
        N_op_total = 0
        for op_hand in opponent_hands:
            # print(f'Opponent cards: {op_hand} \n')

            N_choices = 0
            for action_key in opponent.actions.keys():
                options = self.option_counters[action_key](cards_in_hand=op_hand)
                # print(options)

                if type(options) is list:
                    N_choices += sum([len(i) for i in options])
                else:
                    N_choices += len(options)

            # print(f'\nNumber of choices opponent has for this hand: {N_choices} \n_________________________')
            N_op_total += N_choices

        print(f'\n\nOpponent total options: {N_op_total}\n__________________________')

        # Choose the action randomly for now:
        action_key = random.choice(list(self.actions.keys()))

        # Do the action:
        self.actions[action_key](opponent=opponent)

        # Remove the action from the options:
        self.actions.pop(action_key)
        self.option_counters.pop(action_key)

        # Tell the opponent what we just did:
        if type(opponent) == type(self):
            opponent.opponent_actions.pop(action_key)

    def own_options(self):
        print(f'Cards in my hand: {self.hand} \n')

        N_choices = 0
        for action_key in self.actions.keys():
            options = self.option_counters[action_key](cards_in_hand=self.hand)
            print(options)

            if type(options) is list:
                N_choices += sum([len(i) for i in options])
            else:
                N_choices += len(options)

        print(f'\nNumber of choices I have is: {N_choices} \n_________________________')
