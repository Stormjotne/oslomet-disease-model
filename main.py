from time import sleep
from random import random, uniform

from OMDM import Evolution

"""
Run the model optimization program we're creating from this script.
"""

hyper_parameters = {
    "number_of_generations": 100,
    "genome_length": 10,
    "mutation_probability": 0.5,
    "do_crossover": True,
    "population_size": 100,
    "surviving_individuals": 20,
    "number_of_parents": 20
}

#   Code after this conditional is only executes if the python process originates from this script.
if __name__ == "__main__":
    '''
    Evo = Evolution.Evolution(hyper_parameters)
    #   Run evolution. Printout flag is False by default, so just run the method with no arguments to omit prints.
    result = Evo.evolve(printout=True)
    print("The evolution is complete.\nThe best individual ended up with the following properties:\n")
    print("Fitness: {}\nGenotype: {}\nPhenotype: {}".format(result.fitness, result.genome.genes, result.phenotype))
    '''
    '''
    print("\nTry running it again with an increased number of generations, but remove the printout flag in line 23.")
    '''
    random_number = random()
    print(random_number)
    #   Range:  0.1 - 4.1 meters
    social_distancing = 0.1 + round(random_number * 4, 2)
    print(social_distancing)
    random_number = random()
    #   Range:  1% - 100%
    hand_hygiene = 0.01 + round(random_number * 0.99, 2)
    print(hand_hygiene)
    random_number = random()
    #   Range:  1% - 100%
    respiratory_hygiene = round(0.01 + random_number * 0.99, 2)
    print(respiratory_hygiene)
    random_number = random()
    #   Range:  1% - 100%
    face_masks = 0.01 + round(random_number * 0.99, 2)
    print(face_masks)
    random_number = random()
    #   Range:  1% - 100%
    face_shields = 0.01 + round(random_number * 0.99, 2)
    print(face_shields)
    random_number = random()
    #   Range:  1/8 - 8/8 hour/school day
    key_object_disinfection = (1 + round(random_number * 7)) / 8
    print(key_object_disinfection)
    random_number = random()
    #   Range:  1/16 - 8/16 hour/school day
    surface_disinfection = (1 + round(random_number * 7)) / 16
    print(surface_disinfection)
    random_number = random()
    #   Range:  1 - 3600 seconds
    ventilation_of_indoor_spaces = 1 + round(random_number * 3599)
    print(ventilation_of_indoor_spaces)
    
    