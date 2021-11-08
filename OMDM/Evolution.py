"""

"""
import os
from multiprocessing import Pool, current_process
from time import sleep, time
from datetime import datetime
from random import random, choice, shuffle

from .Population import Population
from .Individual import Individual
from .Model import Model
from . import Data, Fitness


class Evolution:
    """
    Implement the Evolutionary Algorithm in this class.
    """

    def __init__(self, hyper_parameters, printout=False, name="Default"):
        """
        Put any declarations of object fields/variables in this method.
        :param hyper_parameters: Dict
        """
        self.printout = printout
        self.name = name
        self.number_of_threads = os.cpu_count() - 1
        #   Saving the entire dictionary for statistical purposes
        self.hyper_parameters = hyper_parameters
        #   Saving the contents of the dictionary for functional purposes
        self.number_of_generations = hyper_parameters["number_of_generations"]
        self.genome_length = hyper_parameters["genome_length"]
        self.mutation_probability = hyper_parameters["mutation_probability"]
        self.do_crossover = hyper_parameters["do_crossover"]
        self.population_size = hyper_parameters["population_size"]
        self.surviving_individuals = hyper_parameters["surviving_individuals"]
        self.number_of_parents = hyper_parameters["number_of_parents"]
        self.desired_agent_population = hyper_parameters["desired_agent_population"]
        self.desired_agent_population_weight = hyper_parameters["desired_agent_population_weight"]
        self.relative_spread_weight = hyper_parameters["relative_spread_weight"]
        self.best_individual = None
        self.fitness_trend = {}
        self.parameter_trend = {}
        self.generation = 0
        #   Initialize population
        self.population = Population(self.population_size, self.surviving_individuals, self.number_of_parents,
            self.genome_length, self.mutation_probability, do_crossover=self.do_crossover)

    def print_population(self):
        """
        Print the individual objects and their fitness score.
        Only prints the first individual in the sorted list for now.
        """
        print("\nGeneration Best: {}".format(self.population.individuals[0].fitness))
        #   for individ in self.population.individuals:
        #       print("Individual object: {}\nFitness: {}".format(individ, individ.fitness))
        print("\n")

    @staticmethod
    def placeholder_incubate(individual):
        """
        @deprecated
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
        @deprecated
        Generate a phenotype to be evaluated by calling the Model object.
        :param individual:
        :return: Individual's Phenotype
        """
        new_model = Model(individual.genome.genome, normalized=True, static_population=False)
        phenotype = new_model.placeholder_simulate()
        return phenotype
    
    @staticmethod
    def evaluate(individual, d_pop, pop_weight, spread_weight):
        """
        @deprecated
        Evaluate the fitness of an individual in its given environment.
        :param individual:  Individual object
        :param d_pop:   Desired Population
        :type d_pop:    Integer
        :param pop_weight:  The weight of the relative population.
        :type pop_weight:   Float
        :param spread_weight:   The weight of the relative spread of disease.
        :type spread_weight:    Float
        :return: Individual's Fitness
        :rtype: Float
        """
        #   Send the phenotype to a function that calculates its fitness.
        #   fitness = Fitness.relative_spread_fitness(individual.phenotype)
        fitness = Fitness.population_spread_fitness(individual.phenotype, d_pop, pop_weight, spread_weight)
        return fitness
    
    def generate(self, individual):
        """
        Evaluate the fitness of an individual in its given environment.
        :param individual:  Individual object
        :return: Individual
        :rtype: Individual
        """
        if self.printout:
            print(current_process().name, end=" ")
        new_model = Model(
                        individual.genome.genome,
                        self.desired_agent_population,
                        normalized=True,
                        static_population=False,
                        visualize=True
                        )
        individual.phenotype = new_model.simulate()
        individual.fitness = Fitness.population_spread_fitness(
                                individual.phenotype,
                                self.desired_agent_population,
                                self.desired_agent_population_weight,
                                self.relative_spread_weight
                                )
        return individual

    def select_parents(self):
        """
        Select a number of best individuals to serve as the basis for the next generation.
        Use reverse sorting if the fitness functioning is a maximisation problem, otherwise leave it out.
        :return: The best Individuals
        """
        self.population.individuals.sort(key=lambda element: element.fitness)
        #   self.population.individuals.sort(key=lambda element: element.fitness, reverse=True)
        best_individuals = self.population.individuals[:self.number_of_parents]
        return best_individuals
        
    def save_fitness_trend(self):
        """
        Store all the fitness scores in the current population in a list.
        :return:
        :rtype:
        """
        return [x.fitness for x in self.population.individuals]
        
    def save_parameter_trend(self):
        """
        Store all the fitness scores in the current population in a dictionary.
        :return:
        :rtype:
        """
        parameter_dictionary = {}
        for key in self.population.individuals[0].phenotype["parameters"]:
            parameter_dictionary[key] = [x.phenotype["parameters"][key] for x in self.population.individuals]
        return parameter_dictionary
        
    def evolve(self):
        """
        Run the algorithm for a set number of generations.
        Generate a phenotype from the genotype.
        Evaluate the fitness of the phenotype.
        Select parents for the next generation.
        Select the best individual of the generation.
        Populate the next generation by reproduction.
        """
        if self.printout:
            print("Starting evolution.")
            sleep(1)
            print("Found {} available CPU Cores/Threads.".format(self.number_of_threads))
            sleep(1)
        while self.generation < self.number_of_generations:
            #   Wrap the next loop in threads.
            '''for individual in self.population.individuals:
                    #   Create a phenotype from the individual's genotype.
                    individual.phenotype = self.incubate(individual.genome)
                    #   Evaluate the fitness of the individual.
                    individual.fitness = self.evaluate(individual)'''
            #   Use multiprocessing.Pool to generate phenotype and fitness score in parallel.
            with Pool(self.number_of_threads) as process_pool:
                if self.printout:
                    print("\nGeneration number {}.".format(self.generation))
                    print(current_process(), end=" ")
                #   Straight up overwrite population with updated individuals
                #   Maybe there's a nicer way
                self.population.individuals = process_pool.map(self.generate, self.population.individuals)
                process_pool.close()
            #   Do generational printout.
            if self.printout:
                self.print_population()
            #   Select the parents of the next generations.
            #   This method also currently sorts the population by fitness.
            parents = self.select_parents()
            #   Save a pointer to the best individual.
            self.best_individual = self.population.individuals[0]
            #   Save all the fitness scores of the generation
            self.fitness_trend["gen_{}".format(self.generation)] = self.save_fitness_trend()
            #   Save all parameter values of the generation
            self.parameter_trend["gen_{}".format(self.generation)] = self.save_parameter_trend()
            #   Update the next generation by reproduction.
            self.population.individuals = self.population.reproduce(parents)
            #   Iterate
            self.generation += 1
        
        evolutionary_object = {
                "best_individual": self.best_individual,
                "fitness_trend": self.fitness_trend,
                "parameter_trend": self.parameter_trend,
                "hyper_parameters": self.hyper_parameters
                }
        #   Export EA Statistics to JSON and/or plots, etc.
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        Data.export_ea(ea_id=self.name + "_" + timestamp, evo_obj=evolutionary_object)
        #   Return the best individual or whatever else at the end.
        return evolutionary_object


#   Use this conditional to test the class by running it "standalone".
if __name__ == "__main__":
    pass
