"""
Algoritmo Genético en Python

Este código implementa un algoritmo genético básico para encontrar una cadena objetivo
compuesta por 10 caracteres de '1's (es decir, "1111111111"). El algoritmo está inspirado
en los principios de la evolución biológica, como la selección natural, el cruce (crossover)
y la mutación.

El proceso funciona de la siguiente manera:
1. Se crea una población inicial de individuos aleatorios (cadenas de 0s y 1s).
2. Se evalúa la aptitud (fitness) de cada individuo (qué tan cerca está de la solución).
3. Se seleccionan los mejores individuos para reproducirse.
4. Se aplica el cruce (crossover) para crear nuevos individuos (hijos).
5. Se introduce mutación para mantener la diversidad genética.
6. Se repite el proceso hasta encontrar la solución óptima.

Parámetros del algoritmo:
- POPULATION_SIZE: Tamaño de la población.
- GENES: Caracteres posibles en cada gen (en este caso, '0' y '1').
- TARGET: Solución objetivo que queremos encontrar.
- MUTATION_RATE: Probabilidad de que un gen mute.
"""

import random

# Parámetros del algoritmo genético
POPULATION_SIZE = 10  # Tamaño de la población
GENES = "01"  # Genes posibles (binario para este ejemplo)
TARGET = "1111111111"  # Solución objetivo (cadena de 10 unos)
MUTATION_RATE = 0.1  # Probabilidad de mutación (10%)

# Función de aptitud (fitness): Evalúa qué tan cerca está un individuo de la solución
def fitness(individual):
    """
    Calcula la aptitud de un individuo comparándolo con la solución objetivo.
    La aptitud es el número de genes que coinciden con el objetivo.
    """
    return sum(1 for i, j in zip(individual, TARGET) if i == j)

# Crear un individuo aleatorio
def create_individual():
    """
    Genera un individuo aleatorio como una cadena de 0s y 1s.
    """
    return ''.join(random.choice(GENES) for _ in range(len(TARGET)))

# Crear la población inicial
def create_population():
    """
    Crea una población inicial de individuos aleatorios.
    """
    return [create_individual() for _ in range(POPULATION_SIZE)]

# Selección por torneo: Elige el mejor entre dos individuos aleatorios
def selection(population):
    """
    Selecciona dos individuos aleatorios y devuelve el que tiene mayor aptitud.
    """
    return max(random.choices(population, k=2), key=fitness)

# Cruce (crossover): Combina dos individuos para crear un hijo
def crossover(parent1, parent2):
    """
    Realiza el cruce entre dos padres para crear un hijo.
    El punto de cruce se elige aleatoriamente.
    """
    split = random.randint(0, len(TARGET) - 1)
    return parent1[:split] + parent2[split:]

# Mutación: Cambia aleatoriamente algunos genes
def mutate(individual):
    """
    Aplica mutación a un individuo. Cada gen tiene una probabilidad MUTATION_RATE de mutar.
    """
    return ''.join(
        gene if random.random() > MUTATION_RATE else random.choice(GENES)
        for gene in individual
    )

# Algoritmo genético principal
def genetic_algorithm():
    """
    Función principal que ejecuta el algoritmo genético.
    """
    # Crear la población inicial
    population = create_population()
    generation = 1

    while True:
        # Mostrar la población actual
        print(f"Generación {generation}: {population}")

        # Verificar si encontramos la solución
        best_individual = max(population, key=fitness)
        if best_individual == TARGET:
            print(f"\nSolución encontrada en la generación {generation}: {best_individual}")
            break

        # Crear la nueva generación
        new_population = []
        for _ in range(POPULATION_SIZE):
            parent1 = selection(population)
            parent2 = selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        # Reemplazar la población anterior con la nueva
        population = new_population
        generation += 1

# Ejecutar el algoritmo genético
if __name__ == "__main__":
    genetic_algorithm()