from time import sleep

from OMDM.Evolution import Evolution

"""
Run the model optimization program we're creating from this script.
"""

hyper_parameters = {
    "number_of_generations": 10,
    "genome_length": 10,
    "mutation_probability": 0.5,
    "do_crossover": True,
    "population_size": 100,
    "surviving_individuals": 20,
    "number_of_parents": 20
}

#   Code after this conditional is only executes if the python process originates from this script.
if __name__ == "__main__":
    Evo = Evolution(hyper_parameters)
    #   Run evolution. Printout flag is False by default, so just run the method with no arguments to omit prints.
    result = Evo.evolve(printout=True)
    print("The evolution is complete.\nThe best individual ended up with the following properties:\n")
    print("Fitness: {}\nGenotype: {}\nPhenotype: {}".format(result.fitness, result.genotype, result.phenotype))
    print("\nTry running it again with an increased number of generations, but remove the printout flag in line 23.")
