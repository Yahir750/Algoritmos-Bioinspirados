import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import io
import base64
import sys

class AntColonySystem:
    def __init__(
        self,
        distances: np.ndarray,
        n_ants: int = 10,
        iterations: int = 100,
        decay: float = 0.95,
        alpha: float = 1.0,
        beta: float = 2.0,
        q0: float = 0.9,
    ):
        self.distances = distances
        self.n_ants = n_ants
        self.iterations = iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.q0 = q0
        self.n_cities = len(distances)
        self.pheromone = np.ones((self.n_cities, self.n_cities)) / self.n_cities
        self.best_path = None
        self.best_distance = np.inf

    def run(self) -> Tuple[List[int], float]:
        for _ in range(self.iterations):
            paths = self._generate_paths()
            self._update_pheromone(paths)
            current_best_path, current_best_dist = min(paths, key=lambda x: x[1])
            if current_best_dist < self.best_distance:
                self.best_path = current_best_path
                self.best_distance = current_best_dist
        return self.best_path, self.best_distance

    def _generate_paths(self) -> List[Tuple[List[int], float]]:
        paths = []
        for _ in range(self.n_ants):
            path = self._construct_path()
            distance = self._calculate_distance(path)
            paths.append((path, distance))
        return paths

    def _construct_path(self) -> List[int]:
        path = [np.random.randint(0, self.n_cities)]
        visited = set(path)
        while len(visited) < self.n_cities:
            next_city = self._select_next_city(path[-1], visited)
            path.append(next_city)
            visited.add(next_city)
        return path

    def _select_next_city(self, current_city: int, visited: set) -> int:
        unvisited = [city for city in range(self.n_cities) if city not in visited]
        probabilities = np.zeros(len(unvisited))

        for i, city in enumerate(unvisited):
            pheromone = self.pheromone[current_city, city] ** self.alpha
            heuristic = (1 / self.distances[current_city, city]) ** self.beta
            probabilities[i] = pheromone * heuristic

        if np.random.random() < self.q0:
            return unvisited[np.argmax(probabilities)]
        else:
            probabilities /= probabilities.sum()
            return np.random.choice(unvisited, p=probabilities)

    def _calculate_distance(self, path: List[int]) -> float:
        total_distance = 0.0
        for i in range(len(path) - 1):
            total_distance += self.distances[path[i], path[i + 1]]
        total_distance += self.distances[path[-1], path[0]]
        return total_distance

    def _update_pheromone(self, paths: List[Tuple[List[int], float]]) -> None:
        self.pheromone *= self.decay
        for path, distance in paths:
            for i in range(len(path) - 1):
                self.pheromone[path[i], path[i + 1]] += 1 / distance
            self.pheromone[path[-1], path[0]] += 1 / distance

    def plot_path(self, cities: np.ndarray) -> str:
        """Genera un gráfico de la ruta y lo devuelve como imagen en base64"""
        plt.figure(figsize=(10, 6))
        plt.scatter(cities[:, 0], cities[:, 1], c="red", s=100)
        
        # Dibujar todas las ciudades con etiquetas
        for i, city in enumerate(cities):
            plt.annotate(str(i), (city[0] + 1, city[1] + 1))
        
        # Dibujar la mejor ruta
        for i in range(len(self.best_path) - 1):
            plt.plot(
                [cities[self.best_path[i], 0], cities[self.best_path[i + 1], 0]],
                [cities[self.best_path[i], 1], cities[self.best_path[i + 1], 1]],
                "b-",
            )
        
        # Cierre del ciclo
        plt.plot(
            [cities[self.best_path[-1], 0], cities[self.best_path[0], 0]],
            [cities[self.best_path[-1], 1], cities[self.best_path[0], 1]],
            "b-",
        )
        
        plt.title(f"Mejor ruta encontrada (Distancia: {self.best_distance:.2f})")
        
        # Convertir a base64 para Streamlit
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()
        return img_str

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) != 3:
        print("error|Uso: python algoritmo_hormiguero.py <n_ants> <iterations>")
        sys.exit(1)
    
    try:
        # Parámetros desde línea de comandos
        n_ants = int(sys.argv[1])
        iterations = int(sys.argv[2])
        
        # Configuración del problema
        n_cities = 15
        cities = np.random.rand(n_cities, 2) * 100
        distances = np.zeros((n_cities, n_cities))
        
        for i in range(n_cities):
            for j in range(n_cities):
                distances[i, j] = np.linalg.norm(cities[i] - cities[j])
        
        # Ejecutar algoritmo
        acs = AntColonySystem(
            distances,
            n_ants=n_ants,
            iterations=iterations,
            q0=0.8
        )
        
        best_path, best_distance = acs.run()
        img_str = acs.plot_path(cities)
        
        # Salida para Streamlit
        print(f"Mejor distancia {best_distance:.2f}")
        print(f"Mejor ruta {','.join(map(str, best_path))}")
        print(f"image|Ruta visual|{img_str}")
        
    except Exception as e:
        print(f"error|{str(e)}")
        sys.exit(1)