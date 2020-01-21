from game_tools.deck import Deck
from game_tools.scoring import evaluate_game
from agents.random_agent import RandomAgent
from agents.genetic_agent import GeneticAgent
import numpy as np

P1 = GeneticAgent(name='GeneticAgent_1', action_genes=np.random.rand(4, GeneticAgent.n_situ))
P2 = RandomAgent(name='RandomAgent_2')


def game(P1, P2):

    # Init objects:
    d = Deck()

    # Deal cards:
    d.pull_card()
    P1.hand = ''.join([d.pull_card() for _ in range(6)])
    P2.hand = ''.join([d.pull_card() for _ in range(6)])

    # Turns:
    for i in range(4):
        P1.turn(deck=d, opponent=P2)
        P2.turn(deck=d, opponent=P1)

    winner, sd = evaluate_game(P1, P2)
    return winner, sd


winner, sd = game(P1, P2)
print(winner.name, sd)
