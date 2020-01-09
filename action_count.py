import math
import itertools

#     The following functions: return the amount of options an agent has when it has n cards in its hand.
#     Also returns the amount of cards in the next turn. """


def n_choose_k(n, k):
    return int(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))


def secret(n):
    return n_choose_k(n=n, k=1), n


def burn(n):
    return n_choose_k(n=n, k=2), n-1


def gift(n):
    return n_choose_k(n=n, k=3), n-2


def comp(n):
    return n_choose_k(n=n, k=4), n-3


choices = [secret, burn, gift, comp]

N_choices = 0     # Counter for all choices.

# Loop through each permutation of the choices: 24 possibilities
for perm in list(itertools.permutations(choices)):
    N = 7   # Each game you start with 7 cards
    # Loop through the four actions in this permutation and add all choices
    for action in perm:
        n_choices, N = action(N)
        N_choices += n_choices

print(f"The total amount of agent choices independent of specific cards: {int(N_choices)}")