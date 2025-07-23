import os

from minizinc import Instance, Model, Solver


def run_model(model_path:str, dzn_path: str) -> dict:
	"""
	Load a MiniZinc model and DZN data file, solve the instance, and return the solver result.

	Parameters
	----------
	model_path : str
		File path to the MiniZinc model (.mzn). Must exist on disk.
	dzn_path : str
		File path to the MiniZinc data file (.dzn). Must exist on disk.

	Returns
	-------
	dict
		A dictionary containing the solution.

	Raises
	------
	RuntimeError
		If the model_path or dzn_path does not point to an existing file.
	"""
	if not os.path.exists(model_path):
		raise RuntimeError("Error: the provided model path does not exist")

	if not os.path.exists(dzn_path):
		raise RuntimeError("Error: the provided DNZ path does not exist")

	model = Model(model_path)
	model.output_type = dict
	model.add_file(dzn_path)
	solver = Solver.lookup("highs")
	instance = Instance(solver, model)
	result = instance.solve()
	return  result.solution
