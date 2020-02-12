from hanamikoji.game_tools import Deck
import random


def game(agent, opponent):

    # Init objects:
    d = Deck()

    # Deal cards:
    d.pull_card()
    agent.hand = ''.join([d.pull_card() for _ in range(6)])
    opponent.hand = ''.join([d.pull_card() for _ in range(6)])

    players = [agent, opponent]
    random.shuffle(players)

    # Turns:
    for i in range(4):
        players[0].turn(deck=d, opponent=players[1])
        players[1].turn(deck=d, opponent=players[0])

    sd = evaluate_game(agent, opponent)
    agent.reset()
    opponent.reset()
    return sd


def evaluate_game(p1_cards, p2_cards, verbose=False):
    if verbose:
        print('\n EVALUATION:')

    p1_points = 0
    p2_points = 0

    p1_geishas = 0
    p2_geishas = 0

    for key, value in Deck.notation.items():
        p1 = p1_cards.count(key)
        p2 = p2_cards.count(key)

        if p1 > p2:
            if verbose:
                print(f'For card: {key}: Player 1 has won {value} points.')
            p1_points += value
            p1_geishas += 1
        elif p1 < p2:
            if verbose:
                print(f'For card: {key}: Player 2 has won {value} points.')
            p2_points += value
            p2_geishas += 1
        else:
            if verbose:
                print(f'For card: {key}: draw, no points are given')

    if p1_points > p2_points:
        winner = 'Player 1'
    elif p1_points < p2_points:
        winner = 'Player 2'
    else:
        winner = 'NO ONE.'

    if verbose:
        print(f'\n SUMMARY: \n '
              f'>>>> Player 1 has {p1_points} with {p1_geishas} Geishas. \n'
              f' >>>> Player 2 has {p2_points} with {p2_geishas} Geishas. \n'
              f' >>>> >>>> {winner} has won!')

    score_difference = p1_points - p2_points
    return p1_points, p2_points
