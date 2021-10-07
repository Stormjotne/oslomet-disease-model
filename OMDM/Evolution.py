"""

"""
from multiprocessing import Pool, current_process
from time import sleep
from random import random, choice, shuffle

from .Population import Population
from .Individual import Individual
from .Model import Model
from . import Data, Fitness


class Evolution:
    """
    Implement the Evolutionary Algorithm in this class.
    """

    def __init__(self, hyper_parameters):
        """
        Put any declarations of object fields/variables in this method.
        :param hyper_parameters: Dict
        """
        self.number_of_generations = hyper_parameters["number_of_generations"]
        self.genome_length = hyper_parameters["genome_length"]
        self.mutation_probability = hyper_parameters["mutation_probability"]
        self.do_crossover = hyper_parameters["do_crossover"]
        self.population_size = hyper_parameters["population_size"]
        self.surviving_individuals = hyper_parameters["surviving_individuals"]
        self.number_of_parents = hyper_parameters["number_of_parents"]
        self.best_individual = None
        self.generation = 0
        #   Initialize population
        self.population = Population(self.population_size, self.surviving_individuals, self.number_of_parents,
            self.genome_length, self.mutation_probability, do_crossover=self.do_crossover)

    def print_population(self):
        """
        Print the current generation number.
        Print the individual objects and their fitness score.
        """
        print("Generation number {}.\n".format(self.generation))
        print("Generation Best: {}".format(self.population.individuals[0].fitness))
        #   for individ in self.population.individuals:
        #       print("Individual object: {}\nFitness: {}".format(individ, individ.fitness))
        print("\n")

    @staticmethod
    def placeholder_incubate(individual):
        """
        Generate a phenotype to be evaluated.
        :param individual:
        :return: Individual's Phenotype
        """
        #   Fake phenotype
        #   Just sorted genome
        phenotype = sorted(individual.genome.genome)
        return phenotype
        
    @staticmethod
    def incubate(individual):
        """
        Generate a phenotype to be evaluated by calling the Model object.
        :param individual:
        :return: Individual's Phenotype
        """
        new_model = Model(individual.genome, normalized=True, static_population=1000)
        phenotype = new_model.placeholder_simulate()
        return phenotype
    
    @staticmethod
    def evaluate(individual):
        """
        Evalute the fitness of an individual in its given environment.
        :param individual:
        :return: Individual's Fitness
        """
        #   This is just placeholder stuff
        #   Send the phenotype to a function that calculates its fitness.
        fitness = Fitness.relative_spread_fitness(individual.phenotype)
        return fitness

    def select_parents(self):
        """
        Select a number of best individuals to serve as the basis for the next generation.
        :return: The best Individuals
        """
        self.population.individuals.sort(key=lambda element: element.fitness, reverse=True)
        best_individuals = self.population.individuals[:self.number_of_parents]
        return best_individuals
    
    def evolve(self, printout=False):
        """
        Run the algorithm for a set number of generations.
        Generate a phenotype from the genotype.
        Evaluate the fitness of the phenotype.
        Select parents for the next generation.
        Select the best individual of the generation.
        Populate the next generation by reproduction.
        """
        if printout:
            print("Starting evolution.")
            sleep(2)
        while self.generation < self.number_of_generations:
            #   Wrap the next loop in threads.
            for individual in self.population.individuals:
                #   Create a phenotype from the individual's genotype.
                individual.phenotype = self.incubate(individual.genome)
                #   Evaluate the fitness of the individual.
                individual.fitness = self.evaluate(individual)
            #   Do generational printout.
            if printout:
                self.print_population()
            #   Select the parents of the next generations.
            #   This method also currently sorts the population by fitness.
            parents = self.select_parents()
            #   Save a pointer to the best individual.
            self.best_individual = self.population.individuals[0]
            #   Update the next generation by reproduction.
            self.population.individuals = self.population.reproduce(parents)
            #   Iterate
            self.generation += 1
        #   Return the best individual or whatever else at the end.
        return self.best_individual


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
