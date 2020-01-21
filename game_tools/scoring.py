from game_tools.deck import Deck


def evaluate_game(P1, P2, verbose=False):
    if verbose:
        print('\n EVALUATION:')

    p1_points = 0
    p2_points = 0

    p1_geishas = 0
    p2_geishas = 0

    winner_instance = None

    for key, value in Deck.notation.items():
        p1 = P1.cards_placed.count(key)
        p2 = P2.cards_placed.count(key)

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
        winner_instance = P1
        score_difference = p1_points - p2_points

    elif p1_points < p2_points:
        winner = 'Player 2'
        winner_instance = P2
        score_difference = p2_points - p1_points

    else:
        winner = 'NO ONE.'
        score_difference = 0

    if verbose:
        print(f'\n SUMMARY: \n '
              f'>>>> Player 1 has {p1_points} with {p1_geishas} Geishas. \n'
              f' >>>> Player 2 has {p2_points} with {p2_geishas} Geishas. \n'
              f' >>>> >>>> {winner} has won!')

    return winner_instance, score_difference
