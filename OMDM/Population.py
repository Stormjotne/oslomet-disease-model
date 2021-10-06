"""

"""
from random import random

from .Individual import Individual
from .Genome import Genome


class Population:
    """
    Use this class as "loader" of sorts for a collection of model individuals.
    """

    def __init__(self, population_size, surviving_individuals, number_of_parents, genome_length, mutation_probability, do_crossover=False):
        """
        Put any declarations of object fields/variables in this method.
        """
        self.population_size = population_size
        self.surviving_individuals = surviving_individuals
        self.number_of_parents = number_of_parents
        self.genome_length = genome_length
        self.mutation_probability = mutation_probability
        self.do_crossover = do_crossover
        self.individuals = self.populate()

    def populate(self):
        """
        Initialize population of Individuals.
        :return: List of individuals
        """
        list_of_individuals = []
        for individual in range(self.population_size):
            new_individual = Individual(self.mutation_probability, genome_length=self.genome_length)
            list_of_individuals.append(new_individual)
        return list_of_individuals
        
    def reproduce(self, parents):
        """
        Generate offspring and/or random mutations.
        :param parents:
        :return: The Next Generation
        """
        self.individuals.sort(key=lambda element: element.fitness, reverse=True)
        #   Individuals surviving to the next generation.
        retained_adults = self.individuals[:self.surviving_individuals]
        next_generation = retained_adults if retained_adults else []
        i = 0
        if self.do_crossover:
            while len(next_generation) < self.population_size:
                #   Tuple of two parents' genomes.
                parent_genomes = (parents[i].genome.genes, parents[i + 1].genome.genes)
                next_generation.append(Individual(self.mutation_probability, input_genomes=parent_genomes))
                i = (i + 2) % (len(parents) - 1)
        else:
            while len(next_generation) < self.population_size:
                #   Single parent's genome.
                parent_genome = parents[i % self.number_of_parents].genome.genes
                next_generation.append(Individual(self.mutation_probability, input_genes=parent_genome))
                i += 1
        return next_generation


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
