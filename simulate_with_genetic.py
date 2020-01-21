import random
from game_tools.scoring import game
from agents.random_agent import RandomAgent
from agents.genetic_agent import GeneticAgent
import numpy as np


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


# Pairing
def pairing_generator(population_for_mating):
    males = np.random.choice(population_for_mating, size=int(len(population_for_mating)/2), replace=False)
    for m in males:
        try:
            population_for_mating.remove(m)
        except:
            print(males)

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


# Initial generation
generation = []
for i in range(100):
    agent = GeneticAgent(action_genes=np.random.rand(1, len(GeneticAgent.action_permutations)), generation=1, specimen=i)
    generation.append(agent)

# Store data:
score_diff_archive = []
fitness_score_list = []

# Evaluate fitness score:
for i in range(1000):
    fitness_score, fitness_data = fitness_function(generation)
    gen_number = i
    print(f'Generation: {gen_number} fitness score: {fitness_score}. ')
    score_diff_archive.append(fitness_data)
    fitness_score_list.append(fitness_score)

    # Selection:
    generation_sorted = [specimen for _, specimen in sorted(zip(fitness_data, generation))]
    print(f" >>> Best policy: {generation_sorted[-1].root_action_genes} \n")

    elites = generation_sorted[-10:]
    mutate_only = generation_sorted[-20:-10]
    pairing = generation_sorted[-52:-20]

    # New generation
    c = 0
    generation = []

    # The best ones get to go free:
    for e in elites:
        ga = GeneticAgent(action_genes=e.root_action_genes, name="GeneticAgent", generation=i, specimen=c)
        c += 1
        generation.append(ga)

    for m in mutate_only:
        mut_index = np.random.randint(0, m.root_action_genes.shape[1])
        mutated_action_genes = m.root_action_genes
        mutated_action_genes[:, mut_index] -= mutated_action_genes[:, mut_index]
        ga = GeneticAgent(action_genes=mutated_action_genes, name="GeneticAgent", generation=i, specimen=c)
        c += 1
        generation.append(ga)

    # Pairing and Mating:
    for f, m in pairing_generator(population_for_mating=pairing):
        for i in range(5):
            action_genes = single_crossover(f.root_action_genes, m.root_action_genes)

            offspring = GeneticAgent(action_genes=action_genes, generation=i, specimen=c)
            generation.append(offspring)
            c += 1