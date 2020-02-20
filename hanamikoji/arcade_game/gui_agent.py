import numpy.random as rand


class GUIAgent:
    def __init__(self):
        self.action = {'secret': self.secret,
                       'burn': self.burn,
                       'gift': self.gift,
                       'comp': self.comp}

        self.turn_counter = 0

    def turn(self, cards_in_hand):

        action_choice = rand.choice(list(self.action.keys()))
        cards_selected = self.action[action_choice](cards_in_hand)
        self.turn_counter += 1
        self.action.pop(action_choice)

        return action_choice, cards_selected

    def secret(self, cards_in_hand):
        return rand.choice(tuple(cards_in_hand), size=1, replace=False)

    def burn(self, cards_in_hand):
        return rand.choice(tuple(cards_in_hand), size=2, replace=False)

    def gift(self, cards_in_hand):
        return rand.choice(tuple(cards_in_hand), size=3, replace=False)

    def comp(self, cards_in_hand):
        return rand.choice(tuple(cards_in_hand), size=4, replace=False)

    def receive_gift(self, triplet):
        cards_for_me = rand.choice(tuple(triplet), size=1, replace=False)
        cards_for_opponent = triplet
        for c in cards_for_me:
            cards_for_opponent = cards_for_opponent.replace(c, '', 1)

        return cards_for_opponent, ''.join(cards_for_me)

    def receive_comp(self, bundles):
        cards_for_me = rand.choice(tuple(bundles), size=2, replace=False)
        cards_for_opponent = bundles
        for c in cards_for_me:
            cards_for_opponent = cards_for_opponent.replace(c, '', 1)

        return cards_for_opponent, ''.join(cards_for_me)
