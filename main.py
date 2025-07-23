import os

from tools.generate_dzn import generate_dzn
from tools.run_model import run_model


def generate_all_dzn_from_txt() -> None:
	"""
	Traverse a directory of TXT test files, convert each to DZN format, and save to the destination
	directory.

	Raises
	------
	RuntimeError
		If parsing of a TXT file fails in generate_dzn.
	"""
	src_dir = os.path.join("proposed_tests", "TXT")
	dst_dir = os.path.join("proposed_tests", "DZN")

	os.makedirs(dst_dir, exist_ok=True) # Make sure destination exists

	for filename in os.listdir(src_dir):
		if not filename.lower().endswith(".txt"):
			continue

		txt_path = os.path.join(src_dir, filename)
		dzn_name = os.path.splitext(filename)[0] + ".dzn"
		dzn_path = os.path.join(dst_dir, dzn_name)

		try:
			generate_dzn(txt_path, dzn_path)
			print(f"Converted {filename} -> {dzn_name}")
		except Exception as e:
			print(f"Error ({e}): failed converting file {filename}")

def solve_all_dzn() -> None:
	"""
	Solve all .dzn files in the test directory using the MiniZinc model and print results.

	Raises
	------
	RuntimeError
		If the model or a DZN file path does not exist in run_model.
	"""
	dzn_dir = os.path.join("proposed_tests", "DZN")

	for filename in os.listdir(dzn_dir):
		if not filename.lower().endswith(".dzn"):
			continue

		dzn_path = os.path.join(dzn_dir, filename)

		try:
			result = run_model("model.mzn", dzn_path)
		except Exception as e:
			print(f"Error ({e}): failed to solve {dzn_path}")

		print(f"s matrix: {result["s"]}")
		print(f"p_prime: {result["p_prime"]}")
		print(f"Total cost: {result["total_cost"]}")
		print(f"Extremism: {result["extremism"]}")
		print("# ---------------------------------------------------------------------------- #")


if __name__ == "__main__":
	solve_all_dzn()
