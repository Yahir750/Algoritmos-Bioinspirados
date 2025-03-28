# algoritmo_recocido.py
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import streamlit as st


def objective_function(x, y):
    """Función objetivo con múltiples mínimos locales para demostrar el algoritmo"""
    return (np.sin(0.5 * x) ** 2 + np.cos(0.3 * y) + 0.1 * (x ** 2 + y ** 2) ** 0.5)


def run_simulated_annealing(hilo=1, puntos=100, temp_inicial=1000, temp_final=1, enfriamiento=0.95):
    # Configuración inicial
    current_x = random.uniform(-10, 10)
    current_y = random.uniform(-10, 10)
    current_temp = temp_inicial

    # Historial de soluciones para visualización
    history = []
    best_solution = (current_x, current_y)
    best_value = objective_function(current_x, current_y)

    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(10, 8))
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = objective_function(X, Y)

    # Contornos de la función objetivo
    contour = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
    plt.colorbar(contour, label='Valor de la función objetivo')

    # Placeholder para Streamlit
    plot_placeholder = st.empty()

    for i in range(puntos):
        # Generar nueva solución candidata
        new_x = current_x + random.uniform(-hilo, hilo)
        new_y = current_y + random.uniform(-hilo, hilo)

        # Evaluar la función objetivo
        current_value = objective_function(current_x, current_y)
        new_value = objective_function(new_x, new_y)

        # Calcular la probabilidad de aceptación
        if new_value < current_value:
            # Aceptar mejor solución
            current_x, current_y = new_x, new_y
            if new_value < best_value:
                best_solution = (new_x, new_y)
                best_value = new_value
        else:
            # Aceptar peor solución con cierta probabilidad
            prob = math.exp(-(new_value - current_value) / current_temp)
            if random.random() < prob:
                current_x, current_y = new_x, new_y

        # Registrar el historial
        history.append((current_x, current_y))

        # Enfriar el sistema
        current_temp *= enfriamiento

        # Actualizar visualización cada 10 pasos
        if i % 10 == 0 or i == puntos - 1:
            ax.clear()
            ax.contourf(X, Y, Z, levels=20, cmap='viridis')

            # Dibujar todas las trayectorias (hilos)
            if len(history) > 1:
                x_vals, y_vals = zip(*history)
                ax.plot(x_vals, y_vals, 'r-', alpha=0.3, linewidth=1)

            # Dibujar puntos de la trayectoria
            ax.scatter(current_x, current_y, c='red', s=50, label='Posición actual')
            ax.scatter(best_solution[0], best_solution[1], c='yellow', s=100,
                       edgecolors='black', label='Mejor solución')

            # Configuración del gráfico
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_title(f'Recocido Simulado - Iteración {i}\nTemperatura: {current_temp:.2f}')
            ax.legend()

            # Actualizar el gráfico en Streamlit
            plot_placeholder.pyplot(fig)

    return best_solution, best_value


if __name__ == "__main__":
    # Configuración para cuando se ejecute directamente
    import sys

    if len(sys.argv) > 1:
        hilo = float(sys.argv[1])
        puntos = int(sys.argv[2])
    else:
        hilo = 1
        puntos = 100

    best_sol, best_val = run_simulated_annealing(hilo, puntos)
    print(f"Mejor solución encontrada: {best_sol} con valor: {best_val:.4f}")