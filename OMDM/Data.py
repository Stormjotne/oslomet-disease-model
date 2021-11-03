"""
A script containing functions for I/O and data processing.
"""
from pathlib import Path
import json

output_folder = Path("output")


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
	
	save_path = Path(output_folder, ea_id, "parameters.json")
	save_path.parent.mkdir(exist_ok=True, parents=True)
	with open(save_path, "w") as out:
		json.dump(evo_obj["parameter_trend"], out)
