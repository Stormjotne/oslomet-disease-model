from random import random

from Individual import Individual


class Population:
    """
    Use this class as "loader" of sorts for a collection of model individuals.
    """

    def __init__(self, population_size, genome_length):
        """
        Put any declarations of object fields/variables in this method.
        """
        self.population_size = population_size
        self.genome_length = genome_length
        self.individuals = self.populate()

    def populate(self):
        """
        
        :return: List of individuals
        """
        list_of_individuals = []
        for individual in range(self.population_size):
            input_genome = [random() for i in range(self.genome_length)]
            new_individual = Individual(input_genome)
            list_of_individuals.append(new_individual)
        return list_of_individuals


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
