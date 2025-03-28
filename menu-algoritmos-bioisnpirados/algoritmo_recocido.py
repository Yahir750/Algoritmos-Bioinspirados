import numpy as np
import matplotlib.pyplot as plt
import random
import math
import sys
import io
import base64

def objective_function(x, y):
    """Función objetivo con múltiples mínimos locales"""
    return (np.sin(0.5 * x) ** 2 + np.cos(0.3 * y) + 0.1 * (x ** 2 + y ** 2) ** 0.5)

def run_simulated_annealing(hilo=1.0, puntos=100):
    """Algoritmo principal adaptado para Streamlit"""
    # Configuración fija para simplificar
    temp_inicial = 1000
    temp_final = 1
    enfriamiento = 0.95
    
    # Inicialización
    current_x = random.uniform(-10, 10)
    current_y = random.uniform(-10, 10)
    current_temp = temp_inicial
    
    best_solution = (current_x, current_y)
    best_value = objective_function(current_x, current_y)
    
    # Preparar gráfico
    fig, ax = plt.subplots(figsize=(10, 8))
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = objective_function(X, Y)
    
    # Proceso de recocido
    for i in range(iteraciones):
        # Generar nueva solución
        new_x = current_x + random.uniform(-tamaño, tamaño)
        new_y = current_y + random.uniform(-tamaño, tamaño)
        
        # Evaluar solución
        current_value = objective_function(current_x, current_y)
        new_value = objective_function(new_x, new_y)
        
        # Criterio de aceptación
        if new_value < current_value or random.random() < math.exp(-(new_value - current_value) / current_temp):
            current_x, current_y = new_x, new_y
            if new_value < best_value:
                best_solution = (new_x, new_y)
                best_value = new_value
        
        # Enfriar
        current_temp *= enfriamiento
    
    # Generar imagen final
    ax.contourf(X, Y, Z, levels=20, cmap='viridis')
    ax.scatter(best_solution[0], best_solution[1], c='yellow', s=100, 
               edgecolors='black', label=f'Mejor solución: {best_value:.4f}')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_title('Resultado Final - Recocido Simulado')
    ax.legend()
    
    # Convertir a base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return best_solution, best_value, img_str

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("error|Uso: python algoritmo_recocido.py <tamaño> <iteraciones>")
        sys.exit(1)
    
    try:
        tamaño = float(sys.argv[1])
        iteraciones = int(sys.argv[2])
        
        best_sol, best_val, img_str = run_simulated_annealing(tamaño, iteraciones)
        
        print(f"Mejor solución X={best_sol[0]:.4f}, Y={best_sol[1]:.4f}")
        print(f"Valor mínimo {best_val:.4f}")
        print(f"image|Visualización |{img_str}")
        
    except Exception as e:
        print(f"error|{str(e)}")