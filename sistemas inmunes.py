"""
Algoritmo de Sistemas Inmunes Artificiales (AIS) en Python

Este código implementa un algoritmo de sistemas inmunes artificiales para detectar anomalías
en un conjunto de datos. El sistema inmunológico artificial está compuesto por "anticuerpos"
que reconocen y se unen a "antígenos" (patrones anómalos).

El proceso funciona de la siguiente manera:
1. Se genera una población inicial de anticuerpos (soluciones candidatas).
2. Se expone el sistema a un conjunto de datos (antígenos).
3. Se calcula la afinidad entre anticuerpos y antígenos.
4. Se seleccionan los anticuerpos con mayor afinidad y se clonan.
5. Se introduce mutación para mejorar la diversidad.
6. Se repite el proceso hasta que el sistema "aprende" a detectar anomalías.

Parámetros del algoritmo:
- POPULATION_SIZE: Tamaño de la población de anticuerpos.
- DATA_SIZE: Número de antígenos (datos de entrada).
- MUTATION_RATE: Probabilidad de mutación.
- AFFINITY_THRESHOLD: Umbral de afinidad para detectar anomalías.
"""

import random
import numpy as np

# Parámetros del algoritmo
POPULATION_SIZE = 10  # Tamaño de la población de anticuerpos
DATA_SIZE = 20  # Número de antígenos (datos de entrada)
MUTATION_RATE = 0.1  # Probabilidad de mutación
AFFINITY_THRESHOLD = 0.8  # Umbral de afinidad para detectar anomalías

# Función para calcular la afinidad (similitud) entre un anticuerpo y un antígeno
def affinity(antibody, antigen):
    """
    Calcula la afinidad entre un anticuerpo y un antígeno.
    La afinidad es la similitud entre ambos, medida como la proporción de genes iguales.
    """
    return sum(1 for a, b in zip(antibody, antigen) if a == b) / len(antibody)

# Generar un anticuerpo aleatorio
def create_antibody(length):
    """
    Genera un anticuerpo aleatorio como una cadena de 0s y 1s.
    """
    return ''.join(str(random.randint(0, 1)) for _ in range(length))

# Generar una población inicial de anticuerpos
def create_population(pop_size, antibody_length):
    """
    Crea una población inicial de anticuerpos aleatorios.
    """
    return [create_antibody(antibody_length) for _ in range(pop_size)]

# Clonación y mutación de anticuerpos
def clone_and_mutate(antibody, mutation_rate):
    """
    Clona un anticuerpo y aplica mutación a los genes.
    """
    mutated_antibody = ''.join(
        gene if random.random() > mutation_rate else str(1 - int(gene))
        for gene in antibody
    )
    return mutated_antibody

# Algoritmo de Sistemas Inmunes Artificiales
def artificial_immune_system(data, generations=10):
    """
    Función principal que ejecuta el algoritmo de sistemas inmunes.
    """
    antibody_length = len(data[0])  # Longitud de los anticuerpos (igual a la de los antígenos)
    population = create_population(POPULATION_SIZE, antibody_length)

    for generation in range(generations):
        print(f"\nGeneración {generation + 1}:")
        print(f"Población de anticuerpos: {population}")

        # Evaluar la afinidad de cada anticuerpo con los antígenos
        for antigen in data:
            print(f"\nEvaluando antígeno: {antigen}")
            best_antibody = None
            best_affinity = 0

            for antibody in population:
                current_affinity = affinity(antibody, antigen)
                print(f"Afinidad entre {antibody} y {antigen}: {current_affinity:.2f}")

                # Detectar anomalías (afinidad baja)
                if current_affinity < AFFINITY_THRESHOLD:
                    print(f"¡Anomalía detectada! Antígeno: {antigen}, Anticuerpo: {antibody}")

                # Seleccionar el anticuerpo con mayor afinidad
                if current_affinity > best_affinity:
                    best_affinity = current_affinity
                    best_antibody = antibody

            # Clonar y mutar el mejor anticuerpo
            if best_antibody:
                print(f"Mejor anticuerpo: {best_antibody}, Afinidad: {best_affinity:.2f}")
                new_antibody = clone_and_mutate(best_antibody, MUTATION_RATE)
                population.append(new_antibody)
                print(f"Nuevo anticuerpo añadido: {new_antibody}")

# Datos de entrada (antígenos)
data = [
    "1111111111",  # Patrón normal
    "0000000000",  # Patrón normal
    "1010101010",  # Patrón normal
    "1111100000",  # Patrón normal
    "0000011111",  # Patrón normal
    "1111110000",  # Patrón normal
    "1010101010",  # Patrón normal
    "1110001110",  # Patrón normal
    "0001110001",  # Patrón normal
    "1100110011",  # Patrón normal
    "1111111110",  # Posible anomalía
    "0000000011",  # Posible anomalía
    "1010101000",  # Posible anomalía
    "1111100011",  # Posible anomalía
    "0000011100",  # Posible anomalía
    "1111110011",  # Posible anomalía
    "1010101111",  # Posible anomalía
    "1110001100",  # Posible anomalía
    "0001110111",  # Posible anomalía
    "1100110000",  # Posible anomalía
]

# Ejecutar el algoritmo de sistemas inmunes
if __name__ == "__main__":
    artificial_immune_system(data, generations=5)