import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from typing import List, Tuple

st.title("Menú de algoritmos bioinspirados en Streamlit")

# Diccionario de algoritmos disponibles en nuestro menu
algoritmos = {
    "Algoritmo genético": {
        "archivo": "algoritmo genético.py",
        "descripcion": "Descripcion del algoritmo",
        "parametros": {
            "Poblacion": {"key": "poblacion", "tipo": "int"},
            "Mutacion": {"key": "mutacion", "tipo": "float"}
        }
    },
    "Algoritmo inmune": {
        "archivo": "sistemas inmunes.py",
        "descripcion": "Descripcion del algoritmo",
        "parametros": {
            "Enfermedad": {"key": "enfermedad", "tipo": "int"},
            "Cura": {"key": "cura", "tipo": "int"}
        }
    },

    "Algoritmo de hormiguero": {
        "archivo": "Colonia de Hormigas.py",  # Asegúrate de que este archivo existe
        "descripcion": "Algoritmo basado en colonia de hormigas para resolver el problema del vendedor viajero.",
        "parametros": {
            "Número de hormigas": {"key": "n_ants", "tipo": "int"},
            "Número de iteraciones": {"key": "iterations", "tipo": "int"},
            "Tasa de evaporación de feromonas": {"key": "decay", "tipo": "float"},
            "Alpha (peso de las feromonas)": {"key": "alpha", "tipo": "float"},
            "Beta (peso de la heurística)": {"key": "beta", "tipo": "float"},
            "Probabilidad de explotación (q0)": {"key": "q0", "tipo": "float"},
        }},

    "Algoritmo de recocido simulado": {
        "archivo": "algoritmo_recocido.py",
        "descripcion": "Descripcion del algoritmo",
        "parametros": {
            "Hilo": {"key": "hilo", "tipo": "int"},
            "Puntos": {"key": "puntos", "tipo": "int"}
        }
    }
}

# Pestañas

tabs = st.tabs(list(algoritmos.keys()))

# Cada algoritmo con descripcion y parametros en su pestaña
for i, (nombre, datos) in enumerate(algoritmos.items()):
    with tabs[i]:
        st.subheader(nombre)
        st.write(datos["descripcion"])

        parametros = datos["parametros"]
        valores = {}

        for param_name, param_data in parametros.items():
            if param_data["tipo"] == "int":
                valores[param_name] = st.number_input(param_name, min_value=1, step=1, format="%d",
                                                      key=f"{param_data['key']}_{nombre}")
            elif param_data["tipo"] == "float":
                valores[param_name] = st.number_input(param_name, min_value=0.0, step=0.01, format="%f",
                                                      key=f"{param_data['key']}_{nombre}")

        if st.button(f"Ejecutar {nombre}"):
            try:
                resultado = subprocess.run(
                    ["python", datos["archivo"]] + [str(v) for v in valores.values()],
                    capture_output=True,
                    text=True
                )
                st.text_area("Salida:", resultado.stdout)
            except Exception as e:
                st.error(f"Error al ejecutar el algoritmo: {e}")