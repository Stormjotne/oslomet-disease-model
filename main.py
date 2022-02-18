from time import sleep
from random import random, uniform

from OMDM import Evolution

"""
Run the model optimization program we're creating from this script.
"""

hyper_parameters = {
    "number_of_generations":            2,
    "genome_length":                    6,
    "mutation_probability":             0.2,
    "do_crossover":                     True,
    "soft_mutation":                    True,
    "population_size":                  4,
    "surviving_individuals":            2,
    "number_of_parents":                2,
    "desired_agent_population":         500,
    "desired_agent_population_weight":  1,
    "relative_spread_weight":           1
}

#   Code after this conditional is only executes if the python process originates from this script.
if __name__ == "__main__":
    name_of_experiment = "Soft_Mutation_Test"
    Evo = Evolution.Evolution(hyper_parameters, printout=True, name=name_of_experiment)
    #   Run evolution.
    result = Evo.evolve()
    print("The evolution is complete.\nThe best individual ended up with the following properties:\n")
    sleep(1)
    print("Fitness: {}".format(result["best_individual"].fitness))
    sleep(1)
    print("Fitness Trend: {}".format(result["fitness_trend"]))
    sleep(1)
    print("Parameter Trend: {}".format(result["parameter_trend"]))
    sleep(1)
    print("Genotype: {}".format(result["best_individual"].genome.genome))
    sleep(1)
    print("Phenotype: {}".format(result["best_individual"].phenotype))
    