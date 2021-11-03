"""
A script containing functions for I/O and data processing.
"""
from pathlib import Path
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
	save_path = Path(output_folder, ea_id, "fitness.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	with open(save_path, "w") as out:
		json.dump(evo_obj["fitness_trend"], out)
	plot_fitness_trend(save_path, evo_obj["fitness_trend"])
	
	save_path = Path(output_folder, ea_id, "parameters.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	with open(save_path, "w") as out:
		json.dump(evo_obj["parameter_trend"], out)


if __name__ == "__main__":
	output_folder = Path("../output")
	save_path = Path(output_folder, "oneoneone", "fitness.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	plot_fitness_trend(save_path,
							{
							"gen_0":
							[0.36660892388451444, 0.5365974025974026, 0.8040469483568076, 1.116923076923077, 1.15],
							"gen_1":
							[0.3412264631043257, 0.36660892388451444, 0.36923359580052495,
							0.5463376623376623, 0.5463376623376623]})
