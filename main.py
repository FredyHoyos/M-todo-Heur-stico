# Importación de librerías necesarias
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random

# Función principal del algoritmo ACO (colonia de hormigas) en modo iterativo
def aco_iterativo(coords, n_hormigas, n_iteraciones, alpha, beta, rho, Q):
    n = len(coords)
    distancias = np.linalg.norm(coords[:, np.newaxis] - coords[np.newaxis, :], axis=2)
    feromonas = np.ones((n, n))
    mejor_camino = None
    mejor_dist = float('inf')
    iteracion_ultimo_cambio = 0

    # Iteración principal del ACO
    for iteracion in range(n_iteraciones):
        todos_caminos = []
        todas_dist = []

        # Simulación de cada hormiga
        for _ in range(n_hormigas):
            camino = [random.randint(0, n - 1)]
            while len(camino) < n:
                i = camino[-1]
                disponibles = list(set(range(n)) - set(camino))
                probabilidades = []
                for j in disponibles:
                    tau = feromonas[i][j] ** alpha
                    eta = (1 / distancias[i][j]) ** beta
                    probabilidades.append(tau * eta)
                suma = sum(probabilidades)
                probabilidades = [p / suma for p in probabilidades]
                siguiente = random.choices(disponibles, weights=probabilidades)[0]
                camino.append(siguiente)
            camino.append(camino[0])  # Regresa al inicio

            d = sum(distancias[camino[i]][camino[i + 1]] for i in range(n))
            todos_caminos.append(camino)
            todas_dist.append(d)

            # Verifica si es el mejor camino hasta el momento
            if d < mejor_dist:
                mejor_dist = d
                mejor_camino = camino
                iteracion_ultimo_cambio = iteracion + 1

        # Evaporación de feromonas
        feromonas *= (1 - rho)
        for camino, d in zip(todos_caminos, todas_dist):
            for i in range(n):
                a, b = camino[i], camino[i + 1]
                feromonas[a][b] += Q / d
                feromonas[b][a] += Q / d

        yield iteracion + 1, mejor_camino, mejor_dist, iteracion_ultimo_cambio


# Clase de la interfaz gráfica
class ACOApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Colonia de Hormigas - TSP")

        self.ciudades = []
        self.coords_np = None
        self.iterador = None
        self.iter_ultimo_cambio = 0
        self.detener = False

        # Panel lateral de controles
        frame = tk.Frame(root)
        frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)  # <-- margen izquierdo agregado

        labels = ["Hormigas", "Iteraciones", "Alpha", "Beta", "Rho", "Q"]
        defaults = [10, 100, 1.0, 2.0, 0.5, 100.0]
        self.entries = {}

        # Entradas para parámetros del algoritmo
        for label, default in zip(labels, defaults):
            tk.Label(frame, text=label).pack()
            entry = tk.Entry(frame)
            entry.insert(0, str(default))
            entry.pack()
            self.entries[label] = entry

        # Botones de control
        ttk.Button(frame, text="Ejecutar ACO", command=self.ejecutar_aco).pack(pady=10)
        ttk.Button(frame, text="Detener", command=self.detener_animacion).pack(pady=5)
        ttk.Button(frame, text="Limpiar", command=self.limpiar).pack(pady=5)

        # Área para el gráfico
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()
        self.canvas.mpl_connect("button_press_event", self.agregar_ciudad)

        # Configuración inicial del gráfico
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Haz clic para agregar ciudades")
        self.canvas.draw()

    # Agregar ciudad al hacer clic
    def agregar_ciudad(self, event):
        if event.inaxes:
            self.ciudades.append((event.xdata, event.ydata))
            self.redibujar()

    # Limpiar ciudades y gráfico
    def limpiar(self):
        self.ciudades.clear()
        self.ax.clear()
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Haz clic para agregar ciudades")
        self.canvas.draw()

    # Redibuja el gráfico con ciudades y líneas entre ellas
    def redibujar(self):
        self.ax.clear()
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        coords = np.array(self.ciudades)
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                self.ax.plot([coords[i][0], coords[j][0]], [coords[i][1], coords[j][1]], color='gray', linestyle='--', linewidth=0.5)
        self.ax.plot(coords[:, 0], coords[:, 1], 'ro')
        for i, (x, y) in enumerate(coords):
            self.ax.text(x + 1, y + 1, str(i), fontsize=10)
        self.canvas.draw()

    # Ejecuta el algoritmo ACO y comienza la animación
    def ejecutar_aco(self):
        if len(self.ciudades) < 3:
            messagebox.showerror("Error", "Agrega al menos 3 ciudades.")
            return
        try:
            hormigas = int(self.entries["Hormigas"].get())
            iteraciones = int(self.entries["Iteraciones"].get())
            alpha = float(self.entries["Alpha"].get())
            beta = float(self.entries["Beta"].get())
            rho = float(self.entries["Rho"].get())
            Q = float(self.entries["Q"].get())
        except ValueError:
            messagebox.showerror("Error", "Parámetros inválidos.")
            return

        self.coords_np = np.array(self.ciudades)
        self.iterador = aco_iterativo(self.coords_np, hormigas, iteraciones, alpha, beta, rho, Q)
        self.detener = False
        self.animar_iteracion()

    # Detiene la animación
    def detener_animacion(self):
        self.detener = True

    # Anima cada iteración del ACO en la interfaz
    def animar_iteracion(self):
        if self.detener:
            return
        try:
            iteracion, camino, dist, iter_ultimo_cambio = next(self.iterador)
            self.iter_ultimo_cambio = iter_ultimo_cambio

            self.ax.clear()
            self.ax.set_xlim(0, 100)
            self.ax.set_ylim(0, 100)

            # Dibuja líneas grises entre todas las ciudades
            for i in range(len(self.coords_np)):
                for j in range(i + 1, len(self.coords_np)):
                    self.ax.plot(
                        [self.coords_np[i][0], self.coords_np[j][0]],
                        [self.coords_np[i][1], self.coords_np[j][1]],
                        color='gray', linestyle='--', linewidth=0.5
                    )

            # Dibuja el mejor camino actual
            for i in range(len(camino) - 1):
                a, b = camino[i], camino[i + 1]
                self.ax.plot([
                    self.coords_np[a][0], self.coords_np[b][0]
                ], [
                    self.coords_np[a][1], self.coords_np[b][1]
                ], 'b-', linewidth=2)

            # Dibuja las ciudades
            self.ax.plot(self.coords_np[:, 0], self.coords_np[:, 1], 'ro')
            for i, (x, y) in enumerate(self.coords_np):
                self.ax.text(x + 1, y + 1, str(i), fontsize=10)

            # Título con información de la iteración
            self.ax.set_title(f"Iteración {iteracion} - Distancia: {dist:.2f} - Último cambio: {self.iter_ultimo_cambio}")
            self.canvas.draw()
            self.root.after(200, self.animar_iteracion)

        except StopIteration:
            print("Optimización completada.")


# Inicio del programa
if __name__ == "__main__":
    root = tk.Tk()
    app = ACOApp(root)
    root.mainloop()
