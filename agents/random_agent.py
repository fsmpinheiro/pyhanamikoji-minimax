import random
from agents.base_agent import Agent
from combinatoric_tools.tools import choose_from_string


class RandomAgent(Agent):
    def __init__(self, name='RandomAgent__'):
        super().__init__(name)

    def secret(self, opponent):
        card_chosen, self.hand = choose_from_string(string=self.hand, n=1)
        self.cards_placed += card_chosen

        return None

    def burn(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=2)

        return None

    def gift(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=3)
        self.cards_placed += opponent.receive_gift(cards_chosen)

        return cards_chosen

    def comp(self, opponent):
        cards_chosen, self.hand = choose_from_string(string=self.hand, n=4)
        bundle_1, bundle_2 = choose_from_string(cards_chosen, n=2)
        self.cards_placed += opponent.receive_comp([bundle_1, bundle_2])

        return (bundle_1, bundle_2)

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

        # Choose the action completely randomly:
        action_key = random.choice(list(self.actions.keys()))

        print(f"\n {self.name} has hand: {self.hand} and chose action: {action_key}")

        # Do the action:
        cards_played = self.actions[action_key](opponent=opponent)

        # Remove the action from the options:
        self.actions.pop(action_key)

        # Tell the opponent what we just did:
        opponent.receive_info(action_key, cards_played)

