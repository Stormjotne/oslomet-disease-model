"""
A script containing functions for I/O and data processing.
"""
from pathlib import Path
from statistics import median, mean, pvariance, pstdev
import json
import matplotlib.pyplot as plt

output_folder = Path("output")


def plot_fitness_trend(path, fitness_dict):
	"""
	
	@param path:
	@type path:
	@param fitness_dict:
	@type fitness_dict:
	@return:
	@rtype:
	"""
	pass
	

def fitness_stats(fitness_dictionary):
	"""
	Performs mean and standard deviation, minimum and maximum operations on the fitness lists for each generation.
	@param fitness_dictionary:
	@type fitness_dictionary:
	@return:
	@rtype:
	"""
	new_dict = {}
	for key, fitness_list in fitness_dictionary.items():
		new_dict.update({key: {
			"mean": mean(fitness_list),
			"stdev": pstdev(fitness_list),
			"best": min(fitness_list),
			"worst": max(fitness_list)
			}})
	return new_dict
	

def parameter_stats(parameter_dictionary):
	"""
	Performs mean and standard deviation, minimum and maximum operations on all the parameter lists for each generation.
	@param parameter_dictionary:
	@type parameter_dictionary:
	@return:
	@rtype:
	"""
	new_dict = {}
	for key, par_dict in parameter_dictionary.items():
		new_sub_dict = {}
		for sub_key, par_list in par_dict.items():
			new_sub_dict.update({sub_key: {
				"mean": mean(par_list),
				"stdev": pstdev(par_list),
				"min": min(par_list),
				"max": max(par_list)
			}})
		new_dict.update({key: new_sub_dict})
	return new_dict


def export_ea(ea_id, evo_obj):
	"""
	Create JSON files from evolutionary data.
	@param ea_id:
	@type ea_id:
	@param evo_obj:
	@type evo_obj:
	@return:
	@rtype:
	"""
	#  Fitness Trend JSON
	fitness_dictionary = evo_obj["fitness_trend"]
	save_path = Path(output_folder, ea_id, "fitness.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	with open(save_path, "w") as out:
		json.dump(fitness_dictionary, out)
	#  Fitness Stats JSON
	fitness_stats_dictionary = fitness_stats(fitness_dictionary)
	save_path = Path(output_folder, ea_id, "fitness_stats.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	with open(save_path, "w") as out:
		json.dump(fitness_stats_dictionary, out)
	#  Parameter Trend JSON
	parameter_dictionary = evo_obj["parameter_trend"]
	save_path = Path(output_folder, ea_id, "parameters.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	with open(save_path, "w") as out:
		json.dump(parameter_dictionary, out)
	#  Parameter Stats JSON
	parameter_stats_dictionary = parameter_stats(parameter_dictionary)
	save_path = Path(output_folder, ea_id, "parameter_stats.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	with open(save_path, "w") as out:
		json.dump(parameter_stats_dictionary, out)


if __name__ == "__main__":
	output_folder = Path("../output")
	test_name = "Data_Module_Internal_Test"
	fitness_dict = {"gen_0": [0.36660892388451444, 0.5365974025974026, 0.8040469483568076, 1.116923076923077, 1.15], "gen_1": [0.3412264631043257, 0.36660892388451444, 0.36923359580052495, 0.5463376623376623, 0.5463376623376623]}
	parameter_dict = {"gen_0": {"number_of_agents": [486, 388, 388, 352, 244], "social_distancing": [0.31, 3.69, 0.47, 3.19, 2.0], "hand_hygiene": [0.53, 0.81, 0.8, 0.95, 0.96], "face_masks": [0.88, 0.99, 0.72, 0.44, 0.25], "key_object_disinfection": [0.375, 0.375, 0.875, 0.875, 0.5], "face_touching_avoidance": [0.16, 0.72, 0.56, 0.95, 0.34]}, "gen_1": {"number_of_agents": [486, 486, 388, 388, 388], "social_distancing": [0.31, 0.31, 3.69, 3.69, 0.31], "hand_hygiene": [0.81, 0.53, 0.53, 0.81, 0.53], "face_masks": [0.88, 0.88, 0.99, 0.99, 0.88], "key_object_disinfection": [0.375, 0.375, 0.5, 0.375, 0.375], "face_touching_avoidance": [0.16, 0.16, 0.16, 0.72, 0.72]}}
	evo_object = {
                "fitness_trend": fitness_dict,
                "parameter_trend": parameter_dict
             }
	export_ea(test_name, evo_object)
	
	#  plot_fitness_trend(save_path, fitness_dict)
