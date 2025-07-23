import tkinter as tk
from tkinter import filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tools.generate_dzn import generate_dzn, parse_txt
from tools.run_model import run_model


class MiniZincGUI:
	def __init__(self, root):
		self.root = root
		self.root.title("Visualizador de Modelo MiniZinc")
		self.root.geometry("1400x750")  # un poco más ancho para las gráficas

		self.file_path = ""

		# Controles superiores
		top_frame = tk.Frame(root)
		top_frame.pack(pady=5)

		tk.Button(top_frame, text="Seleccionar archivo TXT", command=self.load_txt_file).pack(side=tk.LEFT, padx=5)
		tk.Button(top_frame, text="Ejecutar modelo", command=self.solve_model).pack(side=tk.LEFT, padx=5)

		# Contenedor principal en columnas
		main_frame = tk.Frame(root)
		main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		# Configurar columnas con el mismo peso
		main_frame.grid_columnconfigure(0, weight=1, uniform="col")
		main_frame.grid_columnconfigure(1, weight=1, uniform="col")

		# Columna izquierda - entrada
		self.left_frame = tk.LabelFrame(main_frame, text="Datos de entrada", font=("Arial", 12, "bold"))
		self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

		# Columna derecha - salida
		self.right_frame = tk.LabelFrame(main_frame, text="Resultados", font=("Arial", 12, "bold"))
		self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

		self.labels_input = {}
		self.labels_output = {}

		self.plot1_canvas = None
		self.plot2_canvas = None

	def load_txt_file(self):
		self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
		if not self.file_path:
			return

		try:
			n, m, p, e, ce, c, ct, M = parse_txt(self.file_path)
			self.data = {"n": n, "m": m, "p": p, "e": e, "ce": ce, "c": c, "ct": ct, "M": M}
			self.display_input_data()
			self.plot_initial_distribution(p)
		except Exception as ex:
			messagebox.showerror("Error", str(ex))

	def display_input_data(self):
		for widget in self.left_frame.winfo_children():
			widget.destroy()

		def add_row(key, value, row):
			tk.Label(self.left_frame, text=f"{key}:", anchor="w", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=2, padx=5)
			tk.Label(self.left_frame, text=f"{value}", anchor="w", font=("Arial", 10)).grid(row=row, column=1, sticky="w", pady=2, padx=5)

		data = self.data
		add_row("N° Personas (n)", data["n"], 0)
		add_row("Opiniones posibles (m)", data["m"], 1)
		add_row("Distribución inicial (p)", data["p"], 2)
		add_row("Costo total permitido (ct)", data["ct"], 3)
		add_row("Máximos movimientos (M)", data["M"], 4)

	def solve_model(self):
		if not hasattr(self, "data"):
			messagebox.showwarning("Advertencia", "Primero selecciona un archivo .txt válido.")
			return

		try:
			# Guardar archivo .dzn temporal
			generate_dzn(self.file_path, "DatosProyecto.dzn")

			# Ejecutar modelo
			result = run_model("model.mzn", "DatosProyecto.dzn")

			self.display_output_data(result)
			self.plot_comparison(self.data["p"], result["p_prime"])
		except Exception as ex:
			messagebox.showerror("Error al ejecutar modelo", str(ex))

	def display_output_data(self, result):
		for widget in self.right_frame.winfo_children():
			widget.destroy()

		def add_row(key, value, row):
			tk.Label(self.right_frame, text=f"{key}", anchor="w", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=2, padx=5)
			tk.Label(self.right_frame, text=f"{value}", anchor="w", font=("Arial", 10)).grid(row=row, column=1, sticky="w", pady=2, padx=5)

		add_row("Extremismo final:", result["extremism"], 0)
		add_row("Costo total solución:", result["total_cost"], 1)
		add_row("Distribución final (p'):", result["p_prime"], 2)
		add_row("", "", 3)  # Espacio en blanco para separar
		add_row("", "", 4)  # Espacio en blanco para separar


	def plot_initial_distribution(self, p):
		if self.plot1_canvas:
			self.plot1_canvas.get_tk_widget().destroy()

		fig = Figure(figsize=(6.5, 5), dpi=100)
		ax = fig.add_subplot(111)
		ax.bar(range(1, len(p)+1), p, color="cornflowerblue")
		ax.set_title("Distribución inicial (p)")
		ax.set_xlabel("Opinión")
		ax.set_ylabel("Población")
		ax.set_xticks(range(1, len(p)+1))  # Etiquetas de 1 a m+1 en el eje x

		self.plot1_canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
		self.plot1_canvas.draw()
		self.plot1_canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, pady=10)

	def plot_comparison(self, p, p_prime):
		if self.plot2_canvas:
			self.plot2_canvas.get_tk_widget().destroy()

		fig = Figure(figsize=(6.5, 5), dpi=100)
		ax = fig.add_subplot(111)
		indices = range(1, len(p)+1)
		ax.bar(indices, p, width=0.4, label="p", align="edge", color="salmon")
		ax.bar(indices, p_prime, width=-0.4, label="p'", align="edge", color="mediumseagreen")
		ax.set_title("Comparación: p vs p'")
		ax.set_xlabel("Opinión")
		ax.set_ylabel("Población")
		ax.set_xticks(range(1, len(p)+1))  # Etiquetas de 1 a m+1 en el eje x
		ax.legend()

		self.plot2_canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
		self.plot2_canvas.draw()
		self.plot2_canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
	root = tk.Tk()
	app = MiniZincGUI(root)
	root.mainloop()
