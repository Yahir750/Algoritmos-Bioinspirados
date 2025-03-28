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
import sys

TARGET = "1101110101"
GENES = "01"

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
def create_population(size):
    """
    Crea una población inicial de individuos aleatorios.
    """
    return [create_individual() for _ in range(size)]

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
    split = random.randint(0, len(parent1) - 1)
    return parent1[:split] + parent2[split:]

# Mutación: Cambia aleatoriamente algunos genes
def mutate(individual,mutation_rate):
    """
    Aplica mutación a un individuo. Cada gen tiene una probabilidad MUTATION_RATE de mutar.
    """
    return ''.join(
        gene if random.random() > mutation_rate else random.choice(GENES)
        for gene in individual
    )

# Algoritmo genético principal
def genetic_algorithm(population_size, mutation_rate):
    population = create_population(population_size)
    generation = 1

    while True:
        best_individual = max(population, key=fitness)
        
        if best_individual == TARGET:
            # Solo devolvemos estos dos datos
            return generation, best_individual

        new_population = []
        for _ in range(population_size):
            parent1 = selection(population)
            parent2 = selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population
        generation += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python algoritmo genético.py <poblacion> <mutacion>")
        sys.exit(1)

    try:
        poblacion = int(sys.argv[1])
        mutacion = float(sys.argv[2])
    except ValueError:
        print("Error: Poblacion debe ser un entero y mutacion un decimal (0-1)")
        sys.exit(1)

    generaciones, mejor_individuo = genetic_algorithm(poblacion, mutacion)
    print(f"Generaciones: {generaciones}")
    print(f"Mejor individuo: {mejor_individuo}")