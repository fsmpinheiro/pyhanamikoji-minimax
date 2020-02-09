import random
import numpy as np
import itertools
from agents.base_agent import Agent
from combinatoric_tools.tools import choose_from_string, all_hands

CARD_DECK_SETUP = 'AABBCCDDDEEEFFFFGGGGG'


class GeneticAgent(Agent):

    action_permutations = list(set(itertools.permutations(['secret', 'burn', 'gift', 'comp'])))
    card_types = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    def __init__(self, action_genes, secret_genes, name='GeneticAgent __', generation: int = 0, specimen: int = 0):
        super().__init__(name)
        self.turn_counter = 0

        self.action_genes = np.array(action_genes)
        self.action_genes /= np.linalg.norm(action_genes)

        self.secret_genes = np.array(secret_genes)
        self.secret_genes /= np.linalg.norm(secret_genes)

        self.best_perm = self.action_permutations[int(np.argmax(action_genes))]

        self.action_names = list(self.actions.keys())

        self.generation = generation
        self.specimen = specimen
        self.fitness = -999

        self.root_action_genes = action_genes.copy()
        self.root_secret_genes = self.secret_genes.copy()

    def secret(self, opponent):

        options = set(itertools.combinations(self.hand, 1))
        options = [o[0] for o in sorted(options)]
        distribution = []

        for idx, c_type in enumerate(self.card_types):
            if c_type in options:
                distribution.append(self.secret_genes[idx])

        distribution = np.array(distribution) / sum(distribution)

        card_chosen = np.random.choice(options, p=distribution)
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

    def turn(self, deck, opponent):
        # Pull a card:
        self.hand += deck.pull_card()

        # Decide on the an action:
        action_key = self.best_perm[self.turn_counter]

        # Do the action:
        self.actions[action_key](opponent=opponent)

        self.turn_counter += 1

    def reset(self):
        self.cards_placed = ''
        self.hand = ''

        self.actions = {'secret': self.secret,
                        'burn': self.burn,
                        'gift': self.gift,
                        'comp': self.comp}

        self.action_genes = self.root_action_genes

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness

    def __repr__(self):
        return self.name + str(self.generation) + str(self.specimen)
