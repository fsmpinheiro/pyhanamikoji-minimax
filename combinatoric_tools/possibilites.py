from combinatoric_tools.tools import *
import pandas as pd

card_deck = "AABBCCDDDEEEFFFFGGGGG"

# _______ Case 1: Agent is player 1 _____________________

# All possible hand combinations with 7 cards:
a = all_hands(deck=card_deck, n=7)

# Let's choose 1 random hand:
hand = random.choice(list(a))

deck_remaining = card_deck
for card in hand:
    deck_remaining = deck_remaining.replace(card, '', 1)

print(f'\nAgent Hand: {hand} and deck remaining: {deck_remaining}')


# Agent is player so it will act first:
option_mapping = {'secret': get_secret_options,
                  'burn': get_burn_options,
                  'gift': get_gift_options,
                  'comp': get_comp_options}

N_agent_1 = 0

position = {'hand_1': ''.join(hand),
            'action_1': [],
            'cards_played_1': [],
            'enemy_response': [],
            'enemy_hand_1': [],
            'enemy_action_1:': [],
            'enemy_cards_played_1': [],
            'hand_2': [],
            'action_2': [],
            'cards_played_2': []}

counter = 1

# Loop through all four available actions:
for action_key in option_mapping.keys():
    options = option_mapping[action_key](cards_in_hand=hand)

    # Loop through each card choices:
    for opt in options:

        enemy_response = 'N.A.'
        if action_key == 'gift':
            enemy_responses = set(itertools.combinations(opt, 1))
            for enemy_response in enemy_responses:
                enemy_response = tuple(enemy_response[0])

                position['action_1'].append(action_key)
                position['cards_played_1'].append(opt)
                position['enemy_response'].append(enemy_response)

                counter += 1

        elif action_key == 'comp':
            enemy_responses = set(itertools.combinations([''.join(i) for i in opt], 1))
            for enemy_response in enemy_responses:
                enemy_response = tuple(enemy_response[0])

                position['action_1'].append(action_key)
                position['cards_played_1'].append(opt)
                position['enemy_response'].append(enemy_response)

                counter += 1

        else:
            position['action_1'].append(action_key)
            position['cards_played_1'].append(opt)
            position['enemy_response'].append(enemy_response)

            counter += 1

        # hand_after_this = neg_intersect(hand, flatten(opt))
        # # Loop through all unique card draws in the next turn:
        # for card in set(itertools.combinations(deck_remaining, 1)):
        #
        #     position['action_1'].append(action_key)
        #     position['cards_played_1'].append(opt)
        #     position['hand_2'].append(''.join(join_tuples(hand_after_this, card)))



# Opponent First turn:
opponent_hands = all_hands(deck=deck_remaining, n=7)

print(f'Possible enemy hands: {len(opponent_hands)} \n')

# For each opponent hand, the opponent can choose 4 actions
N_enemy_1 = 0

for idx, hand in enumerate(opponent_hands):

    secret_options = set(itertools.combinations(hand, 1))
    # print(f'Secret: {secret_options}')

    burn_options = set(itertools.combinations(hand, 2))
    # print(f'Burn: {burn_options}')

    gift_options = set(itertools.combinations(hand, 3))
    # print(f'Gift: {gift_options}')

    comp_options = get_comp_options(hand)
    # print(f'Comp: {comp_options} \n')

    N_enemy_options = len(secret_options) + len(burn_options) + len(gift_options) + sum([len(i) for i in comp_options])

    # print(f'{idx+1}: Enemy hand: {hand} >>>> options with this hand in turn {1}: {N_enemy_options}')

    N_enemy_1 += N_enemy_options

print(f'\n \n Total Enemy options in turn {1}: {N_enemy_1} __________________________')
