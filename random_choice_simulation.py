from deck import Deck
from agent import Agent

# Init objects:
d = Deck()
P1 = Agent(name='Player_1')
P2 = Agent(name='Player_2')

# Deal cards:
d.pull_card()
P1.hand = ''.join([d.pull_card() for _ in range(6)])
P2.hand = ''.join([d.pull_card() for _ in range(6)])

# Turns:
for i in range(4):
    P1.turn(deck=d, opponent=P2)

    P2.turn(deck=d, opponent=P1)

# Print Status:
P1.status()
P2.status()


def evaluate_game(p1_placed, p2_placed):

    p1_points = 0
    p2_points = 0

    p1_geishas = 0
    p2_geishas = 0

    for key, value in Deck.notation.items():
        p1 = p1_placed.count(key)
        p2 = p2_placed.count(key)

        if p1 > p2:
            print(f'For card: {key}: Player 1 has won {value} points.')
            p1_points += value
            p1_geishas += 1
        elif p1 < p2:
            print(f'For card: {key}: Player 2 has won {value} points.')
            p2_points += value
            p2_geishas += 1
        else:
            print(f'For card: {key}: draw, no points are given')

    if p1_points >= 11 or p1_geishas >= 4:
        winner = 'Player 1'
    elif p2_points >= 11 or p2_geishas >= 4:
        winner = 'Player 2'
    else:
        if p1_points > p2_points:
            winner = 'Player 1'
        elif p1_points < p2_points:
            winner = 'Player 2'
        else:
            winner = 'NO ONE.'

    print(f'\n SUMMARY: \n '
          f'>>>> Player 1 has {p1_points} with {p1_geishas} Geishas. \n'
          f' >>>> Player 2 has {p2_points} with {p2_geishas} Geishas. \n'
          f' >>>> >>>> {winner} has won!')


evaluate_game(P1.cards_placed, P2.cards_placed)
