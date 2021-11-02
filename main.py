from time import sleep
from random import random, uniform

from OMDM import Evolution

"""
Run the model optimization program we're creating from this script.
"""

hyper_parameters = {
    "number_of_generations":            1,
    "genome_length":                    6,
    "mutation_probability":             0.2,
    "do_crossover":                     True,
    "population_size":                  10,
    "surviving_individuals":            5,
    "number_of_parents":                5,
    "desired_agent_population":         500,
    "desired_agent_population_weight":  1,
    "relative_spread_weight":           1
}

#   Code after this conditional is only executes if the python process originates from this script.
if __name__ == "__main__":
    Evo = Evolution.Evolution(hyper_parameters, printout=True)
    #   Run evolution.
    result = Evo.evolve()
    print("The evolution is complete.\nThe best individual ended up with the following properties:\n")
    sleep(1)
    print("Fitness: {}".format(result.fitness))
    sleep(1)
    print("Genotype: {}".format(result.genome.genome))
    sleep(1)
    print("Phenotype: {}".format(result.phenotype))
    