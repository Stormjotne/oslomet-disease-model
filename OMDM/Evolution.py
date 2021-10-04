"""

"""
from multiprocessing import Pool, current_process
from time import sleep
from random import random, choice, shuffle

from .Population import Population
from .Individual import Individual
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
        self.population = Population(self.population_size, self.genome_length)

    def print_population(self):
        """
        Print the current generation number.
        Print the individual objects and their fitness score.
        """
        print("Generation number {}.\n".format(self.generation))
        for individ in self.population.individuals:
            print("Individual object: {}\nFitness: {}".format(individ, individ.fitness))
        print("\n")
        sleep(1)

    @staticmethod
    def incubate(individual):
        """
        Generate a phenotype to be evaluated.
        :param individual:
        :return: Individual's Phenotype
        """
        #   Fake phenotype
        #   Just sorted genome
        phenotype = sorted(individual.genome.genes)
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
        fitness = Fitness.placeholder_fitness(individual.phenotype)
        return fitness

    def select_parents(self, individuals):
        """
        Select a number of best individuals to serve as the basis for the next generation.
        :param individuals:
        :return: The best Individuals
        """
        individuals.sort(key=lambda element: element.fitness, reverse=True)
        best_individuals = individuals[:self.number_of_parents]
        return best_individuals
    
    def reproduce(self, parents, individuals):
        """
        Generate offspring and/or random mutations.
        :param parents:
        :param individuals:
        :return: The Next Generation
        """
        individuals.sort(key=lambda element: element.fitness, reverse=True)
        #   Individuals surviving to the next generation.
        retained_adults = individuals[:self.surviving_individuals]
        next_generation = retained_adults if retained_adults else []
        i = 0
        if self.do_crossover:
            while len(next_generation) < self.population_size:
                new_genes = self.crossover(parents[i].genome.genes, parents[i + 1].genome.genes)
                next_generation.append(Individual(input_genome=new_genes))
                i = (i + 2) % (len(parents) - 1)
        else:
            while len(next_generation) < self.population_size:
                new_genes = self.clone(parents[i % self.number_of_parents].genome.genes)
                next_generation.append(Individual(input_genome=new_genes))
                i += 1
        return next_generation
    
    def clone(self, parent_genome):
        """
        Create new genome from parent's genome with a chance of mutation.
        :param parent_genome:
        """
        genes = []
        for gene in parent_genome:
            genes.append(random() if random() < self.mutation_probability else gene)
        return genes

    def crossover(self, parent_genome_one, parent_genome_two):
        """
        Create new genome from two parents' genomes with a chance of mutation.
        :param parent_genome_one:
        :param parent_genome_two:
        """
        genes = []
        for gene1, gene2 in zip(parent_genome_one, parent_genome_two):
            genes.append(random() if random() < self.mutation_probability else choice((gene1, gene2)))
        return genes
    
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
            print("The goal of this EA is to converge the mean value in the genome to a certain target value,"
                  " with as little variance as possible.")
            sleep(5)
            print("You'll see at the end that the phenotype will be a sorted list"
                  " where the mean value is very close to 0.5 with (hopefully) very little variance.")
            sleep(5)
            print("Starting evolution.")
            sleep(2)
        while self.generation < self.number_of_generations:
            for individual in self.population.individuals:
                individual.phenotype = self.incubate(individual)
                individual.fitness = self.evaluate(individual)
            #   Print all individuals and their fitness
            if printout:
                self.print_population()
            parents = self.select_parents(self.population.individuals)
            self.best_individual = self.population.individuals[0]
            self.population.individuals = self.reproduce(parents, self.population.individuals)
            self.generation += 1
        return self.best_individual


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
