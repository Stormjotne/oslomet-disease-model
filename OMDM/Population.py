import Model
from random import random

class Population:
    """
    Use this class as "loader" of sorts for a collection of model individuals.
    """

    def __init__(self, population_size):
        """
        Put any declarations of object fields/variables in this method.
        """
        pass

    def __individuals(self):
        """

        :return: List of individuals
        """
        list_of_individuals = []
        for individual in range(self.population_size):
            g = [random() for i in range(self.genome)]
            list_of_individuals.append(Individual(g))
        return list_of_individuals


class Individual:
    """
    Use this class initialize model individuals.
    """

    def __init__(self, genotype):
        """
        Put any declarations of object fields/variables in this method.
        :param genome:
        """
        pass


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
