class Agent:
    def __init__(self, name):
        self.name = name
        self.hand = ''
        self.cards_placed = ''

        self.actions = {'secret': self.secret,
                        'burn': self.burn,
                        'gift': self.gift,
                        'comp': self.comp}

    def secret(self, opponent):
        pass

    def burn(self, opponent):
        pass

    def gift(self, opponent):
        pass

    def comp(self, opponent):
        pass

    def receive_gift(self, triplet):
        pass

    def receive_comp(self, bundles):
        pass

    def turn(self, deck, opponent):
        raise NotImplementedError

    def status(self):
        self.hand = ''.join(sorted(self.hand))
        self.cards_placed = ''.join(sorted(self.cards_placed))
        print(f'{self.name}: with hand: {self.hand} and cards placed: {self.cards_placed}')

    def receive_info(self, *args, **kwargs):
        pass
