import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple  # Para anotaciones de tipo (mejora la legibilidad)

class AntColonySystem:
    def __init__(
        self,
        distances: np.ndarray,  # Matriz de distancias entre ciudades
        n_ants: int = 10,       # Número de hormigas
        iterations: int = 100,  # Número de iteraciones
        decay: float = 0.95,    # Tasa de evaporación de feromonas
        alpha: float = 1.0,     # Peso de las feromonas en la selección
        beta: float = 2.0,      # Peso de la heurística (1/distancia)
        q0: float = 0.9,        # Probabilidad de explotación (elegir el mejor camino)
    ):
        self.distances = distances
        self.n_ants = n_ants
        self.iterations = iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.q0 = q0
        self.n_cities = len(distances)
        # Inicialización de feromonas: valores pequeños y uniformes
        self.pheromone = np.ones((self.n_cities, self.n_cities)) / self.n_cities
        self.best_path = None     # Mejor ruta encontrada
        self.best_distance = np.inf  # Distancia de la mejor ruta

    def run(self) -> Tuple[List[int], float]:
        """Ejecuta el algoritmo ACS y devuelve la mejor ruta y su distancia."""
        for _ in range(self.iterations):
            # 1. Generar rutas para todas las hormigas
            paths = self._generate_paths()
            # 2. Actualizar feromonas basado en las rutas
            self._update_pheromone(paths)
            # 3. Actualizar la mejor solución global
            current_best_path, current_best_dist = min(paths, key=lambda x: x[1])
            if current_best_dist < self.best_distance:
                self.best_path = current_best_path
                self.best_distance = current_best_dist
        return self.best_path, self.best_distance

    def _generate_paths(self) -> List[Tuple[List[int], float]]:
        """Genera rutas para todas las hormigas."""
        paths = []
        for _ in range(self.n_ants):
            path = self._construct_path()  # Construye una ruta aleatoria
            distance = self._calculate_distance(path)  # Calcula su distancia
            paths.append((path, distance))
        return paths

    def _construct_path(self) -> List[int]:
        """Construye una ruta para una hormiga usando reglas de transición ACS."""
        path = [np.random.randint(0, self.n_cities)]  # Ciudad inicial aleatoria
        visited = set(path)
        while len(visited) < self.n_cities:
            next_city = self._select_next_city(path[-1], visited)  # Elige próxima ciudad
            path.append(next_city)
            visited.add(next_city)
        return path

    def _select_next_city(self, current_city: int, visited: set) -> int:
        """Selecciona la próxima ciudad basado en feromonas y heurística."""
        unvisited = [city for city in range(self.n_cities) if city not in visited]
        probabilities = np.zeros(len(unvisited))

        # Calcula probabilidades para cada ciudad no visitada
        for i, city in enumerate(unvisited):
            pheromone = self.pheromone[current_city, city] ** self.alpha
            heuristic = (1 / self.distances[current_city, city]) ** self.beta
            probabilities[i] = pheromone * heuristic

        # Regla de transición ACS: explotación (q0) o exploración (1-q0)
        if np.random.random() < self.q0:
            # Explotación: elegir la ciudad con mayor probabilidad
            return unvisited[np.argmax(probabilities)]
        else:
            # Exploración: elegir basado en probabilidad normalizada
            probabilities /= probabilities.sum()
            return np.random.choice(unvisited, p=probabilities)

    def _calculate_distance(self, path: List[int]) -> float:
        """Calcula la distancia total de una ruta (incluyendo volver al inicio)."""
        total_distance = 0.0
        # Suma las distancias entre ciudades consecutivas
        for i in range(len(path) - 1):
            total_distance += self.distances[path[i], path[i + 1]]
        # Agrega la distancia de retorno al inicio
        total_distance += self.distances[path[-1], path[0]]
        return total_distance

    def _update_pheromone(self, paths: List[Tuple[List[int], float]]) -> None:
        """Actualiza las feromonas: evaporación + depósito por las hormigas."""
        # 1. Evaporación global
        self.pheromone *= self.decay
        # 2. Depósito de feromonas (solo en las rutas usadas)
        for path, distance in paths:
            for i in range(len(path) - 1):
                self.pheromone[path[i], path[i + 1]] += 1 / distance
            # Feromona en el último tramo (volver al inicio)
            self.pheromone[path[-1], path[0]] += 1 / distance

# --- Ejemplo de uso ---
if __name__ == "__main__":
    #np.random.seed(42)  # Para reproducibilidad / comentado para que sea ramdom la semilla :)
    n_cities = 15
    # Generar ciudades aleatorias en un plano 2D
    cities = np.random.rand(n_cities, 2) * 100
    # Calcular matriz de distancias (euclidianas)
    distances = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            distances[i, j] = np.linalg.norm(cities[i] - cities[j])

    # Configurar y ejecutar ACS
    acs = AntColonySystem(
        distances,
        n_ants=15,
        iterations=200,
        decay=0.95,
        alpha=1,
        beta=3,
        q0=0.8,  # 80% de probabilidad de explotación
    )
    best_path, best_distance = acs.run()

    # Resultados
    print(f"Mejor ruta: {best_path}")
    print(f"Distancia total: {best_distance:.2f}")

    # Visualización
    plt.figure(figsize=(10, 6))
    plt.scatter(cities[:, 0], cities[:, 1], c="red", s=100)
    for i, city in enumerate(cities):
        plt.annotate(str(i), (city[0] + 1, city[1] + 1))
    # Dibujar la ruta
    for i in range(len(best_path) - 1):
        plt.plot(
            [cities[best_path[i], 0], cities[best_path[i + 1], 0]],
            [cities[best_path[i], 1], cities[best_path[i + 1], 1]],
            "b-",
        )
    # Cierre del ciclo (volver al inicio)
    plt.plot(
        [cities[best_path[-1], 0], cities[best_path[0], 0]],
        [cities[best_path[-1], 1], cities[best_path[0], 1]],
        "b-",
    )
    plt.title(f"ACS - Mejor ruta (Distancia: {best_distance:.2f})")
    plt.show()