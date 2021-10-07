"""
A script containing functions for calculating the fitness score of an individual.
"""
from math import fabs
from statistics import median, mean, pvariance

from . import Data


def population_spread_fitness(input_phenotype):
	"""
	Reward high population of agents, punish high spread of disease.
	:param input_phenotype:
	:type input_phenotype:
	:return:
	:rtype:
	"""
	pass
	

def relative_spread_fitness(input_phenotype):
	"""
	Punish high spread of disease.
	:param input_phenotype:
	:type input_phenotype:
	:return:
	:rtype:
	"""
	infected = input_phenotype["number_total_infected"]
	agents = input_phenotype["number_of_agents"]
	relative_spread = infected / agents
	return 1 - relative_spread


def placeholder_fitness(input_phenotype):
	"""
	Just a placeholder fitness function.
	:param input_phenotype:
	"""
	target_value = 0.5
	target_variance = 0
	#   The score is 1 minus the distance between the average of all genes and the target value
   #   The mean and median values of the genome, divided by two.
	#   phenotype = (mean(individual.genotype) + median(individual.genotype)) / 2
	average_of_input = mean(input_phenotype)
	variance_of_input = pvariance(input_phenotype)
	#  distance from target
	mean_distance = fabs(target_value - average_of_input)
	variance_distance = fabs(target_variance - variance_of_input)
	#  1 is maximum possible fitness. Subtract distances.
	fitness = 1 - mean_distance - variance_distance
	return fitness
