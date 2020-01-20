from combinatoric_tools.tools import *

card_deck = "AABBCCDDDEEEFFFFGGGGG"

# _______ Case 1: Agent is player 1 _____________________

# All possible hand combinations with 7 cards:
a = all_hands(deck=card_deck, n=7)

# Let's choose 1 random hand:
hand = random.choice(list(a))

deck_remaining = card_deck
for card in hand:
    deck_remaining = deck_remaining.replace(card, '', 1)

opponent_hands = all_hands(deck=deck_remaining, n=7)

print(f'\n Hand: {hand} and Deck remaining: {deck_remaining}')
print(f'Possible enemy hands: {len(opponent_hands)} \n')

# For each opponent hand, the opponent can choose 4 actions
N = 0

for hand in opponent_hands:
    print(f"Opponent's hand: {hand}")

    secret_options = set(itertools.combinations(hand, 1))
    print(f'Secret: {secret_options}')

    burn_options = set(itertools.combinations(hand, 2))
    print(f'Burn: {burn_options}')

    gift_options = set(itertools.combinations(hand, 3))
    print(f'Gift: {gift_options}')

    comp_options = get_comp_options(hand)
    print(f'Comp: {comp_options} \n')

    N_enemy_options = len(secret_options) + len(burn_options) + len(gift_options) + sum([len(i) for i in comp_options])

    print(f'\n Enemy options with this hand: {N_enemy_options} \n')

    N += N_enemy_options


print(f'\n \n Total Enemy options: {N}')

