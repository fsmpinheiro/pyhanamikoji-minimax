import random

from game_tools.deck import Deck
from game_tools.scoring import evaluate_game, game
from agents.random_agent import RandomAgent
from agents.genetic_agent import GeneticAgent
import numpy as np

N_population = 100

N_elites = 10
N_mutate_only = 10
N_survivors = 32
N_offsprings = 5


# Fitness function: play 100 games against an the random agent opponent:
def fitness_function(generation):
    opponent = RandomAgent(name='RandomAgent')
    sd_list = []

    for specimen in generation:
        sd = game(agent=specimen, opponent=opponent)
        specimen.fitness = sd

        sd_list.append(sd)
    sd_list = np.array(sd_list)
    fitness_score_pop = len(sd_list[sd_list > 0]) / len(generation)
    return fitness_score_pop, sd_list


# Initial generation
generation = []
for i in range(100):
    agent = GeneticAgent(action_genes=np.random.rand(4, GeneticAgent.n_situ), generation=1, specimen=i)
    generation.append(agent)

# Evaluate fitness score:
fitness_score, fitness_data = fitness_function(generation)
gen_number = 0
print(f'Generation: {gen_number} fitness score: {fitness_score}')

# Selection:
generation_sorted = [specimen for _, specimen in sorted(zip(fitness_data, generation))]
elites = generation_sorted[-10:]
mutate_only = generation_sorted[-20:-10]
pairing = generation_sorted[-52:-20]


# Pairing
def pairing_generator(population_for_mating):
    males = np.random.choice(population_for_mating, size=16)
    for m in males:
        population_for_mating.remove(m)

    females = population_for_mating
    assert len(females) == len(males)

    for i in range(len(females)):
        yield females[i], males[i]


# Mating:
def single_crossover(f_mat, m_mat):
    crossover_point = random.randint(0, f_mat.shape[1])

    new_kid = np.zeros(shape=f_mat.shape)
    new_kid[:, :crossover_point] = f_mat[:, :crossover_point]
    new_kid[:, crossover_point:] = m_mat[:, crossover_point:]

    return new_kid


offsprings = []

for f, m in pairing_generator(population_for_mating=pairing):
    for i in range(5):
        action_genes = single_crossover(f.root_action_genes, m.root_action_genes)

        offspring = GeneticAgent(action_genes=action_genes)
        offsprings.append(offspring)


generation = []
[generation.append(e) for e in elites]
[generation.append(m) for m in mutate_only]
[generation.append(o) for o in offsprings]

# print(generation)

fitness_score, fitness_data = fitness_function(generation)
gen_number = 1
print(f'Generation: {gen_number} fitness score: {fitness_score}')