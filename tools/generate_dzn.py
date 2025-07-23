def parse_txt(
	path: str
) -> tuple[int, int, list[int], list[float], list[float], list[list[float]], float, int]:
	"""
	Parse a text file into its constituent data parameters.

	Parameters
	----------
		path (str): path to the input TXT file.

	Returns
	-------
		tuple: (n, m, p, e, ce, c, ct, M) where:
			n : int
				Total number of people.
			m : int
				Number of opinion categories.
			p : list[int]
				Population distribution per category.
			e : list[float]
				Extremism values per category.
			ce : list[float]
				Extra cost values per category with zero initial population.
			c :list[list[float]]
				m x m cost matrix.
			ct : float
				Total allowed cost.
			M : int
				Maximum number of moves allowed.

	Raises
	------
		RuntimeError: if the file cannot be parsed or format is invalid.
	"""
	try:
		with open(path, "r") as f:
			lines = [l.strip() for l in f]

		it = iter(lines)
		n = int(next(it))
		m = int(next(it))
		p = list(map(int, next(it).split(",")))
		e = list(map(float, next(it).split(",")))
		ce = list(map(float, next(it).split(",")))
		c = [list(map(float, next(it).split(","))) for _ in range(m)]
		ct = float(next(it))
		M = int(next(it))

		return n, m, p, e, ce, c, ct, M

	except Exception as e:
		raise RuntimeError(f"Error ({e}): parsing the TXT file in {path}")

def to_dzn(
	n: int,
	m: int,
	p: list[int],
	e: list[float],
	ce: list[float],
	c: list[list[float]],
	ct: float,
	M: int
) -> str:
	"""
	Generate a MiniZinc .dzn content string from parsed parameters.

	Parameters
	----------
		n : int
			Total number of people.
		m : int
			Number of opinion categories.
		p : list[int]
			Population distribution per category.
		e : list[float]
			Extremism values per category.
		ce : list[float]
			Extra cost values per category with zero initial population.
		c :list[list[float]]
			m x m cost matrix.
		ct : float
			Total allowed cost.
		M : int
			Maximum number of moves allowed.

	Returns
	-------
		str: the formatted DZN content as a string.
	"""
	lines: list[str] = []
	lines.append(f"n = {n};")
	lines.append(f"m = {m};")
	lines.append("")

	lines.append(f"p = [{', '.join(map(str, p))}];")
	lines.append(f"e = [{', '.join(map(str, e))}];")
	lines.append(f"ce = [{', '.join(map(str, ce))}];")
	lines.append("")

	lines.append("c = [|")
	c_elements = len(c)
	for i in range(c_elements):
		suffix = '' if i == c_elements - 1 else '|'

		lines.append('\t' + ", ".join(map(str, c[i])) + suffix)
	lines.append("|];\n")

	lines.append(f"ct = {ct};")
	lines.append(f"M = {M};")

	return '\n'.join(lines)

def generate_dzn(source: str, destination: str) -> None:
	"""
	High-level function that orchestrates parsing of the input TXT file
	and generation of the corresponding MiniZinc .dzn file.

	Parameters
	----------
	source : str
		Path to the source TXT file containing the raw input data.
	destination : str
		Path where the generated .dzn file should be saved.

	Raises
	------
	RuntimeError: if parsing the TXT file fails or writing to the output DZN file fails.
	"""
	n, m, p, e, ce, c, ct, M = parse_txt(source)
	dzn_content = to_dzn(n, m, p, e, ce, c, ct, M)

	try:
		with open(destination, "w") as f:
			f.write(dzn_content)

	except Exception as e:
		raise RuntimeError(f"Error ({e}): writing the DZN file in {destination}")
