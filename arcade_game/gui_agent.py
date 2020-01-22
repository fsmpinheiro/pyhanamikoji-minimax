import random


class GUIAgent:
    def __init__(self):
        self.action = {'secret': self.secret,
                       'burn': self.burn,
                       'gift': self.gift,
                       'comp': self.comp}

    def turn(self, cards_in_hand):



        return cards_in_hand, cards_placed, cards_burned

    def secret(self, cards_in_hand):
        pass

    def burn(self, cards_in_hand):
        pass

    def gift(self, cards_in_hand):
        pass

    def comp(self, cards_in_hand):
        pass

    def receive_gift(self, triplet):
        pass

    def receive_comp(self, bundles):
        pass
