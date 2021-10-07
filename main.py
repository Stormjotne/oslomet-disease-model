from time import sleep
from random import random, uniform

from OMDM import Evolution

"""
Run the model optimization program we're creating from this script.
"""

hyper_parameters = {
    "number_of_generations": 100,
    "genome_length": 9,
    "mutation_probability": 0.2,
    "do_crossover": True,
    "population_size": 10,
    "surviving_individuals": 2,
    "number_of_parents": 2
}

#   Code after this conditional is only executes if the python process originates from this script.
if __name__ == "__main__":
    Evo = Evolution.Evolution(hyper_parameters)
    #   Run evolution. Printout flag is False by default, so just run the method with no arguments to omit prints.
    result = Evo.evolve(printout=True)
    print("The evolution is complete.\nThe best individual ended up with the following properties:\n")
    print("Fitness: {}\nGenotype: {}\nPhenotype: {}".format(result.fitness, result.genome.genome, result.phenotype))
    '''
    print("\nTry running it again with an increased number of generations, but remove the printout flag in line 23.")
    '''
    
    