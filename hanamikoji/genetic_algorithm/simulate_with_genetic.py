from agents.random_agent import RandomAgent
from agents.genetic_agent import GeneticAgent
import numpy as np
import matplotlib.pyplot as plt
from hanamikoji.genetic_algorithm.genetic import fitness_function, pairing_generator

POPULATION_SIZE = 200
ELITE_SIZE = 10
MUTATION_ONLY_SIZE = 10
OFFSPRING_COUNT = 5
PARING_SIZE = int(2 * (200 - ELITE_SIZE - MUTATION_ONLY_SIZE) / 5)
MAX_GENERATIONS = 10000


# Initial generation
opponent = RandomAgent()
generation = []
for i in range(POPULATION_SIZE):
    agent = GeneticAgent(action_genes=np.random.rand(len(GeneticAgent.action_permutations)),
                         secret_genes=np.random.rand(len(GeneticAgent.card_types)),
                         generation=0, specimen=i)
    generation.append(agent)

# Store data:
score_diff_archive = []
fitness_score_list = []

# Evaluate fitness score:
for i in range(MAX_GENERATIONS):
    fitness_score, fitness_data = fitness_function(generation, opponent=opponent)
    gen_number = i+1
    if gen_number % 20 == 0:
        print(f'Generation: {gen_number} fitness score: {fitness_score}. ')

    score_diff_archive.append(fitness_data)
    fitness_score_list.append(fitness_score)

    # Selection:
    generation_sorted = [specimen for _, specimen in sorted(zip(fitness_data, generation))]

    elites = generation_sorted[-ELITE_SIZE:]

    mutate_slice = -ELITE_SIZE-MUTATION_ONLY_SIZE
    mutate_only = generation_sorted[mutate_slice:-ELITE_SIZE]

    pairing_slice = mutate_slice - PARING_SIZE
    pairing = generation_sorted[pairing_slice:mutate_slice]

    # New generation
    c = 0
    generation = []

    # The best ones get to go free:
    for e in elites:
        ga = GeneticAgent(action_genes=e.root_action_genes, secret_genes=e.root_secret_genes, name="GeneticAgent",
                          generation=i, specimen=c)
        c += 1
        generation.append(ga)

    for m in mutate_only:
        mut_index = np.random.randint(0, m.root_action_genes.shape[0])
        mutated_action_genes = m.root_action_genes
        mutated_action_genes[mut_index] = 2.0 * mutated_action_genes[mut_index]
        ga = GeneticAgent(action_genes=mutated_action_genes, secret_genes=m.root_secret_genes, name="GeneticAgent",
                          generation=i, specimen=c)
        c += 1
        generation.append(ga)

    # Pairing and Mating:
    for f, m in pairing_generator(population_for_mating=pairing):
        for _ in range(5):

            # todo: Write mating code with proper gene model.
            action_genes = 0.8 * f.root_action_genes + 0.2 * m.root_action_genes
            secret_genes = 0.8 * f.root_secret_genes + 0.2 * m.root_secret_genes

            offspring = GeneticAgent(action_genes=action_genes, secret_genes=secret_genes, generation=i, specimen=c)
            generation.append(offspring)
            c += 1

plt.plot(fitness_score_list)
plt.show()
