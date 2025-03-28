import math
import random

# Función Objetivo: Función Rastrigin
def objective_function(x):
    """
    Calcula el valor de la función Rastrigin para un vector x.
    La función Rastrigin es conocida por tener múltiples mínimos locales.
    """
    return 10 * len(x) + sum([(xi**2 - 10 * math.cos(2 * math.pi * xi)) for xi in x])

# Función para obtener un vecino: realiza un pequeño cambio aleatorio en una posición
def get_neighbor(x, step_size=0.1):
    """
    Genera una nueva solución vecina modificando uno de los valores de x aleatoriamente.
    """
    # Copiar la solución actual y modificar un valor aleatoriamente
    neighbor = x[:]
    index = random.randint(0, len(x) - 1) 
    neighbor[index] += random.uniform(-step_size, step_size) 
    return neighbor

# Función de Recocido Simulado
def simulated_annealing(objective, bounds, n_iterations, step_size, temp):
    """
    Realiza el algoritmo de Recocido Simulado para encontrar la mejor solución posible
    en un espacio de búsqueda dado.
    """
    # Inicialización de la solución
    best = [random.uniform(bound[0], bound[1]) for bound in bounds] 
    best_eval = objective(best)
    current, current_eval = best, best_eval
    scores = [best_eval]

    # Iterar por el número de iteraciones especificado
    for i in range(n_iterations):
        # Reducir la temperatura en cada iteración
        t = temp / float(i + 1)

        # Generar una nueva solución vecina
        candidate = get_neighbor(current, step_size)
        candidate_eval = objective(candidate)

        # Decidir si aceptamos la nueva solución
        if candidate_eval < best_eval or random.random() < math.exp((current_eval - candidate_eval) / t):
            current, current_eval = candidate, candidate_eval
            if candidate_eval < best_eval:
                best, best_eval = candidate, candidate_eval
                scores.append(best_eval)

        # Imprimir el progreso opcionalmente
        if i % 100 == 0:
            print(f"Iteración {i}, Temperatura {t:.3f}, Mejor Evaluación {best_eval:.5f}")

    return best, best_eval, scores

# Definición del dominio del problema (espacio de búsqueda)
bounds = [(-5.0, 5.0) for _ in range(2)]
n_iterations = 1000
step_size = 0.1
temp = 10

# Ejecutar la búsqueda utilizando Recocido Simulado
best, score, scores = simulated_annealing(objective_function, bounds, n_iterations, step_size, temp)

# Mostrar los resultados
print(f'Solución Óptima: {best}')
print(f'Mejor Puntaje: {score}')
