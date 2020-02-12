from hanamikoji.game_tools.scoring import game
import numpy as np
import random


def fitness_function(generation, opponent):
    """ Fitness function: play 100 games against an opponent. Gather the score differences and the amoun of wins."""
    sd_list = []

    for specimen in generation:
        sd = game(agent=specimen, opponent=opponent)
        specimen.fitness = sd

        sd_list.append(sd)
    sd_list = np.array(sd_list)
    fitness_score_pop = len(sd_list[sd_list > 0]) / len(generation)
    return fitness_score_pop, sd_list


def pairing_generator(population_for_mating):
    """ Takes a list of objects and pairs them up randomly. """
    assert len(population_for_mating) % 2 == 0

    males = np.random.choice(population_for_mating, size=int(len(population_for_mating)/2), replace=False)
    for m in males:
        population_for_mating.remove(m)

    females = population_for_mating

    for i in range(len(females)):
        yield females[i], males[i]


def single_point_crossover(f_gene, m_gene):
    """ Generates a random cross over point and creates an offspring gene set from the two parent."""

    crossover_point = random.randint(f_gene.shape[0])

    new_gene = np.zeros(shape=f_gene.shape)
    new_gene[crossover_point] = f_gene[:crossover_point]
    new_gene[crossover_point:] = m_gene[crossover_point:]

    return new_gene


